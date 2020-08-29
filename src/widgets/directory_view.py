"""
------------------------------------------------------------------------------
    @file       directory_view.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Directory view.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
import os, shutil
from PyQt5                          import QtWidgets, QtCore, QtGui
from src.utils.asset_system         import AssetSystem
from src.utils.log_system           import LogSystem
from src.utils.action_system        import ActionSystem
from src.widgets.syntax_highlighter import SyntaxHighlighter

class IconProviderWidget(QtWidgets.QFileIconProvider):
    """
    Custom icon provider for our directory view widget.
    """
    def icon(self, file_info):
        if file_info.isDir():
            return AssetSystem.icons["DIR"]     # If it is folder return folder icon.
        else:
            return AssetSystem.icons["FILE"]    # If it is file return file icon.

class DirectoryViewWidget(object):

    def __init__(self, main_form):
        """
        Constructs directory view widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """
        Intialize all widgets for directory view widget.
        """
        self.hidden = True
        
        self.directory_view_window = QtWidgets.QDockWidget("Directory view", self.main_form)
        self.main_form.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.directory_view_window)
        self.directory_view_window.visibilityChanged.connect(self.directory_view_window_visibility_callback)

        self.current_working_directory = None

        self.filesystem = QtWidgets.QFileSystemModel()
        self.filesystem.setIconProvider(IconProviderWidget())

        self.directory_view_tree = QtWidgets.QTreeView()
        self.directory_view_tree.setAnimated(False)
        self.directory_view_tree.clicked.connect(self.directory_view_tree_item_clicked_callback)
        self.directory_view_tree.setStyleSheet("QTreeView { border: 1px solid lightgrey; }")
        self.directory_view_window.setWidget(self.directory_view_tree)
        self.directory_view_window.hide()

        self.directory_view_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.directory_view_tree.customContextMenuRequested.connect(self.custom_menu_context)

    # Getter for directory view window
    @property
    def dock(self): return self.directory_view_window

    # Getter for directory view tree
    @property
    def tree(self): return self.directory_view_tree

    # Getter for current working directory
    @property
    def cwd(self): return self.current_working_directory

    # Setter for current working directory
    @cwd.setter
    def cwd(self, value):  self.current_working_directory = value
    
    def directory_view_window_visibility_callback(self, visible):
        """
        Change visibility status for directory view widget.
        """
        self.hidden = not visible

    def directory_view_tree_item_clicked_callback(self, item):
        """
        Ppen clicked file from directory view in new tab.
        """
        file_path = self.filesystem.filePath(item)

        if os.path.isfile(file_path):
            LogSystem.success("Opening file: {0}".format(file_path))
            ActionSystem.new_file(file_path)
        else:
            LogSystem.warning("Selected item is not file!")

    def custom_menu_context(self, point):
        """
        Custom context menu for directory view widget.
        """
        if not self.current_working_directory:
            return

        index         = self.directory_view_tree.currentIndex()
        file_path     = self.filesystem.filePath(index)
        selected_item = self.directory_view_tree.indexAt(point)
        menu          = QtWidgets.QMenu()

        if selected_item.data(QtCore.Qt.DisplayRole) == None:
            LogSystem.success("Requested context menu for current working directory!")
            action_1 = menu.addAction("Create new file")
            action_1.triggered.connect(lambda: self.create_new_file(self.current_working_directory))
            action_2 = menu.addAction("Create new directory")
            action_2.triggered.connect(lambda: self.create_new_folder(self.current_working_directory))
        elif os.path.isfile(file_path):
            LogSystem.success("Requested context menu for file: {0}!".format(file_path))
            action_1 = menu.addAction("Open")
            action_1.triggered.connect(lambda: self.open_file_in_new_tab(file_path))
            action_2 = menu.addAction("Rename")
            action_2.triggered.connect(lambda: self.rename_file(file_path))
            action_3 = menu.addAction("Delete")
            action_3.triggered.connect(lambda: self.delete_file_from_dir_view(file_path))
        else:
            LogSystem.success("Requested context menu for directory: {0}!".format(file_path))
            action_1 = menu.addAction("Rename")
            action_1.triggered.connect(lambda: self.rename_file(file_path))
            action_2 = menu.addAction("Delete")
            action_2.triggered.connect(lambda: self.delete_file_from_dir_view(file_path))
            action_3 = menu.addAction("Create new directory")
            action_3.triggered.connect(lambda: self.create_new_folder(file_path))
            action_3 = menu.addAction("Create new file")
            action_3.triggered.connect(lambda: self.create_new_file(file_path))

        menu.exec_(self.directory_view_tree.mapToGlobal(point))


    def open_file_in_new_tab(self, file_path):
        """
        Open file in new tab.
        """
        try:
            ActionSystem.new_file(file_path)
        except Exception as e:
            LogSystem.error(e)

    def create_new_file(self, file_path):
        """
        Create new file.
        """
        try:
            text, ok = QtWidgets.QInputDialog.getText(self.main_form, "Create new file", "Name:")
            if ok and text:
                with open(file_path + "/" + text, "w") as _:
                    LogSystem.success("Created new file: {0}".format(file_path + "/" + text))
                    pass
        except Exception as e:
            LogSystem.error(e)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setIcon(QtWidgets.QMessageBox.Critical)
            error_message_box.setText("Error")
            error_message_box.setInformativeText("{0}".format(e))
            error_message_box.setWindowTitle("Failed to create file")
            error_message_box.exec_()

    def create_new_folder(self, file_path):
        """
        Crete new folder.
        """
        try:
            text, ok = QtWidgets.QInputDialog.getText(self.main_form, "Create new file", "Name:")
            if ok and text:
                os.mkdir(file_path + "/" + text)
                LogSystem.success("Created new folder: {0}".format(file_path + "/" + text))
        except Exception as e:
            LogSystem.error(e)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setIcon(QtWidgets.QMessageBox.Critical)
            error_message_box.setText("Error")
            error_message_box.setInformativeText("{0}".format(e))
            error_message_box.setWindowTitle("Failed to create directory")
            error_message_box.exec_()

    def rename_file(self, file_path):
        """
        Rename file.
        """
        try:
            text, ok = QtWidgets.QInputDialog.getText(self.main_form, "Rename file", "New name:")
            if ok:
                paths     = file_path.split("/")
                paths[-1] = text
                new_path  = "/".join(paths)

                os.rename(file_path, new_path)
                for tab in self.main_form.tab_bar.tabs:
                    if tab.file_path == file_path:
                        tab.file_path = new_path
                        tab.title     = text
                        tab.extension = text.split(".")[-1]

                        if tab.extension == "asm":
                            tab.syntax = SyntaxHighlighter(tab.textarea.document(), file_path)
                        else:
                            if tab.syntax:
                                del tab.syntax
                            tab.syntax = None
                            _T = tab.textarea.toPlainText()
                            tab.textarea.setPlainText(_T)
                        self.main_form.tab_bar.get.setTabText(self.main_form.tab_bar.get.indexOf(tab.widget), text)
                        break

        except Exception as e:
            LogSystem.error(e)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setIcon(QtWidgets.QMessageBox.Critical)
            error_message_box.setText("Error")
            error_message_box.setInformativeText("Invalid name was given!")
            error_message_box.setWindowTitle("Failed to rename file")
            error_message_box.exec_()

    def delete_file_from_dir_view(self, file_path):
        """
        Delete file.
        """
        try:
            answer = QtWidgets.QMessageBox.question(self.main_form, "WARNING", "This will permanently remove file/directory from system.\nDo you wish to proceed?",
                     QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                if os.path.isfile(file_path):
                    for tab in self.main_form.tab_bar.tabs:
                        if tab.file_path == file_path:
                            self.main_form.tab_bar.remove(tab)
                            break
                    os.remove(file_path)
                else:
                    LogSystem.success("Deleted: {0}".format(file_path))
                    shutil.rmtree(file_path)
        except Exception as e:
            LogSystem.error(e)
