"""
------------------------------------------------------------------------------
    @file       action_system.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Action system form IDE.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

import datetime
from PyQt5                          import QtWidgets, QtCore, QtGui
from src.utils.log_system           import LogSystem
from src.widgets.syntax_highlighter import SyntaxHighlighter
from src.hack_compiler              import HackAssemblyCompiler, InvalidSyntaxException, InternalException

class ActionSystem(object):

    main_form = None

    @classmethod
    def initialize(cls, main_form):
        """
        Set action for specific form, in our case we want these actions on our main form.
        """
        cls.main_form = main_form

    @classmethod
    def new_file(cls, file_path=None):
        """
        Create new file and open a new tab for that file, if file path is not provided it will only open empty tab.
        """
        LogSystem.information("Creating new file")
        cls.main_form.tab_bar.create_new_tab(file_path)

    @classmethod
    def open_file(cls):
        """
        Open file dialog to select specific file to open in new tab.
        """
        LogSystem.information("Open file")
        try:
            options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, ok = QtWidgets.QFileDialog.getOpenFileName(cls.main_form, "Open File", options=options)
            
            if ok:
                cls.new_file(file_path)
        except Exception as e:
            LogSystem.error(e)

    @classmethod
    def open_folder(cls):
        """
        Open file dialog to select specific folder to open and will show directory view dock.
        """
        LogSystem.information("Open folder")
        try:
            options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
            directory_path = QtWidgets.QFileDialog.getExistingDirectory(cls.main_form, "", "./repository", options=options)

            if directory_path:
                LogSystem.success("Opening directory: {0}".format(directory_path))
                cls.main_form.directory_view.dock.show()
                cls.main_form.directory_view.filesystem.setRootPath(directory_path)
                cls.main_form.directory_view.tree.setModel(cls.main_form.directory_view.filesystem)
                cls.main_form.directory_view.tree.setRootIndex(cls.main_form.directory_view.filesystem.index(directory_path))
                for col in range(1, 4):
                    cls.main_form.directory_view.tree.hideColumn(col)
                cls.main_form.directory_view.cwd = directory_path
            else:
                LogSystem.warning("Ignoring open folder request!")
        except Exception as e:
            LogSystem.error(e)

    @classmethod
    def save_file(cls):
        """
        Open file dialog for saving files.
        """
        LogSystem.information("Save file")
        try:
            current_tab = cls.main_form.tab_bar.current
            if not current_tab.file_path:
                LogSystem.information("Opening save file dialog!")
                options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
                file_path, ok = QtWidgets.QFileDialog.getSaveFileName(cls.main_form, "Save file", options=options)
                if ok:
                    for tab in cls.main_form.tab_bar.tabs:
                        if tab.file_path == file_path:
                            cls.main_form.tab_bar.remove(tab)

                    current_tab.file_path = file_path
                    current_tab.title     = file_path.split("/")[-1]
                    current_tab.extension = file_path.split(".")[-1]

                    try:
                        if current_tab.extension == "asm":
                            current_tab.syntax = SyntaxHighlighter(current_tab.textarea.document(), file_path)
                    except Exception as e:
                        LogSystem.error(e)

                    cls.main_form.tab_bar.get.setTabText(cls.main_form.tab_bar.get.indexOf(current_tab.widget), current_tab.title)

            if not current_tab.saved and current_tab.file_path:
                LogSystem.success("Saving file: {0}".format(current_tab.file_path))
                text_buffer = current_tab.textarea.toPlainText()
                file_path   = current_tab.file_path

                with open(file_path, "w") as file:
                    file.write(text_buffer)

                current_tab.saved = True
            else:
                LogSystem.warning("No changes made to file: {0}".format(current_tab.file_path))

        except Exception as e:
            LogSystem.error(e)

    @classmethod
    def save_file_as(cls):
        """
        Open file dialog for saving files.
        """
        LogSystem.information("Save file as")
        try:
            current_tab = cls.main_form.tab_bar.current
            options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, ok = QtWidgets.QFileDialog.getSaveFileName(cls.main_form, "Save file", options=options)

            if ok:
                current_tab.file_path = file_path
                current_tab.title     = file_path.split("/")[-1]
                current_tab.extension = file_path.split(".")[-1]
                current_tab.saved = True
                cls.main_form.tab_bar.get.setTabText(cls.main_form.tab_bar.get.indexOf(current_tab.widget), current_tab.title)

                try:
                    if current_tab.extension == "asm":
                        current_tab.syntax = SyntaxHighlighter(current_tab.textarea.document(), file_path)
                except Exception as e:
                    LogSystem.error(e)

                text_buffer = current_tab.textarea.toPlainText()
                file_path   = current_tab.file_path

                with open(file_path, "w") as file:
                    file.write(text_buffer)
                LogSystem.information("File saved as: {0}".format(file_path))

        except Exception as e:
            LogSystem.error(e)

    @classmethod
    def load_comparison_file(cls):
        """
        Load hack file for comparison and display comparison dock widget.
        """
        LogSystem.information("Starting Action Load Comparison File!")
        try:
            options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, ok = QtWidgets.QFileDialog.getOpenFileName(cls.main_form, "Open File", "./repository", "Hack files (*.hack)", options=options)
            
            if ok:
                with open(file_path, "r") as file:
                    cls.main_form.comparison_dock.list.clear()
                    cls.main_form.comparison_dock.file = file_path
                    text_buffer = file.read().split("\n")

                    for line in text_buffer:
                        if line:
                            list_item = QtWidgets.QListWidgetItem(line)
                            cls.main_form.comparison_dock.list.addItem(list_item)

                cls.main_form.comparison_dock.show()
        except Exception as e:
            LogSystem.error(e)


    @classmethod
    def clear_comparison_file(cls):
        """
        Clear content in comparison dock widget.
        """
        LogSystem.information("Starting Action Clear Comparison File!")
        try:
            cls.main_form.comparison_dock.list.clear()
            cls.main_form.comparison_dock.file = None
        except Exception as e:
            LogSystem.error(e)

    @classmethod
    def compile(cls):
        """
        Compile hack assembly code that is opened in current tab.
        """
        LogSystem.information("Starting Action Compile!")
        try:
            # Check if file was saved
            current_tab = cls.main_form.tab_bar.current

            if not current_tab.saved:
                cls.save_file()
                if current_tab.saved == False:
                    return

            file_path = current_tab.file_path

            cls.main_form.destination_dock.pc        = None
            cls.main_form.destination_dock.file_path = None
            cls.main_form.compilation_dock.textarea.clear()
            cls.main_form.compilation_dock.show()
            cls.main_form.compilation_dock.textarea.appendPlainText("Time: {0}".format(datetime.datetime.now()))

            cls.main_form.destination_dock.dock.show()
            cls.main_form.tab_bar.current.textarea.setExtraSelections([])

            for i in range(cls.main_form.comparison_dock.list.count()):
                cls.main_form.comparison_dock.list.item(i).setBackground(QtGui.QColor(255, 255, 255))

            try:
                cls.main_form.destination_dock.list.clear()

                hack_assembly_compiler = HackAssemblyCompiler(file_path, "temp.hack")
                hack_assembly_compiler.compile()

                for binary in hack_assembly_compiler.binary_data:
                    list_item = QtWidgets.QListWidgetItem(binary)
                    cls.main_form.destination_dock.list.addItem(list_item)

                cls.main_form.compilation_dock.textarea.appendPlainText("Compilation: Success... ✔️")
                cls.main_form.destination_dock.pc = hack_assembly_compiler.program_counter_and_lines.copy()
                cls.main_form.destination_dock.file_path = cls.main_form.tab_bar.current.file_path

            except InvalidSyntaxException as e:
                LogSystem.error("Invalid syntax error")
                
                error_msg  = str(e)
                error_line = ""
                error      = ""
                for i in range(len(error_msg)):
                    if error_msg[i] == ":":
                        error = error_msg[i+1:]
                        break
                    error_line += error_msg[i]

                cls.main_form.destination_dock.pc = None
                cls.main_form.compilation_dock.textarea.appendPlainText("Compilation: Error on line {0} - {1} ❌".format(error_line, error))
                cls.main_form.tab_bar.current.textarea.highlightErrorLine(int(error_line) - 1)
                return
            except InternalException as e:
                LogSystem.error("Internal error")
                cls.main_form.destination_dock.pc = None
                cls.main_form.compilation_dock.textarea.appendPlainText("Compilation: Error {0} ❌".format(e))
                return
            except Exception as e:
                LogSystem.error(e)
                cls.main_form.destination_dock.pc = None
                cls.main_form.compilation_dock.textarea.appendPlainText("Compilation: Error {0} ❌".format(e))
                return


            if not cls.main_form.comparison_dock.file:
                return

            destination_items_counter = cls.main_form.destination_dock.list.count()
            comparison_items_counter  = cls.main_form.comparison_dock.list.count()

            max_items = destination_items_counter if destination_items_counter > comparison_items_counter else comparison_items_counter
            min_items = destination_items_counter if destination_items_counter < comparison_items_counter else comparison_items_counter

            try:
                for i in range(max_items):
                    try:
                        destination_item = cls.main_form.destination_dock.list.item(i).text()
                    except:
                        cls.main_form.comparison_dock.list.item(i).setBackground(QtGui.QColor(255, 255, 100))
                        cls.main_form.compilation_dock.textarea.appendPlainText("Comparison: Failed - There are more lines of code in comparison file! ❌")
                        return

                    try:
                        comparison_item = cls.main_form.comparison_dock.list.item(i).text()
                    except:
                        cls.main_form.destination_dock.list.item(i).setBackground(QtGui.QColor(255, 255, 100))
                        cls.main_form.compilation_dock.textarea.appendPlainText("Comparison: Failed at line {0} ❌".format(hack_assembly_compiler.program_counter_and_lines[i]))
                        cls.main_form.tab_bar.current.textarea.highlightComparisonLine(int(hack_assembly_compiler.program_counter_and_lines[i]) - 1)
                        return

                    if destination_item == comparison_item:
                        cls.main_form.destination_dock.list.item(i).setBackground(QtGui.QColor(170, 255, 170))
                        cls.main_form.comparison_dock.list.item(i).setBackground(QtGui.QColor(170, 255, 170))
                    else:
                        cls.main_form.destination_dock.list.item(i).setBackground(QtGui.QColor(255, 255, 100))
                        cls.main_form.comparison_dock.list.item(i).setBackground(QtGui.QColor(255, 255, 100))
                        
                        cls.main_form.compilation_dock.textarea.appendPlainText("Comparison: Failed at line {0} ❌".format(hack_assembly_compiler.program_counter_and_lines[i]))
                        cls.main_form.tab_bar.current.textarea.highlightComparisonLine(int(hack_assembly_compiler.program_counter_and_lines[i]) - 1)
                        return

                cls.main_form.compilation_dock.textarea.appendPlainText("Comparison: Success... ✔️")

            except Exception as e:
                LogSystem.error(e)

        except Exception as e:
            LogSystem.error(e)


    @classmethod
    def export_destination(cls):
        """
        Save compiled data.
        """
        try:
            if cls.main_form.destination_dock.list.count() == 0:
                LogSystem.warning("Nothing to export!")
                dialog = QtWidgets.QMessageBox()
                dialog.setIcon(QtWidgets.QMessageBox.Information)
                dialog.setText("Exporting")
                dialog.setInformativeText("There is nothing to export!")
                dialog.setWindowTitle("Export information")
                dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                dialog.exec_()
                return

            options = QtWidgets.QFileDialog.Option() | QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, ok = QtWidgets.QFileDialog.getSaveFileName(cls.main_form, "Save file", ".hack", "Hack files (*.hack)", options=options)
            if ok:
                with open(file_path, "w") as file:
                    for i in range(cls.main_form.destination_dock.list.count()):
                        destination_item = cls.main_form.destination_dock.list.item(i).text()
                        file.write(destination_item + "\n")
                LogSystem.warning("Destination saved to: {0}".format(file_path))

        except Exception as e:
            LogSystem.error(e)