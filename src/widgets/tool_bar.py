"""
------------------------------------------------------------------------------
    @file       tool_bar.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Tool bar.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5                   import QtWidgets, QtCore, QtGui
from src.utils.action_system import ActionSystem
class ToolBarWidget(object):

    def __init__(self, main_form):
        """
        Constructs tool bar widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()


    def initialize_all_widgets(self):
        """
        Initialize all widgets that exist in tool bar widget.
        """
        self.hidden   = False
        self.tool_bar = self.main_form.findChild(QtWidgets.QToolBar, "toolBar")
        self.tool_bar.setStyleSheet("QToolBar { border: none;}")

        self.new_button = QtWidgets.QPushButton()
        self.new_button.setIcon(QtGui.QIcon("./assets/icons/new_file.svg"))
        self.new_button.setToolTip("Create New File")
        self.tool_bar.addWidget(self.new_button)
        self.new_button.clicked.connect(ActionSystem.new_file)

        self.open_folder_button = QtWidgets.QPushButton()
        self.open_folder_button.setIcon(QtGui.QIcon("./assets/icons/default_folder_opened.svg"))
        self.open_folder_button.setToolTip("Open Folder")
        self.tool_bar.addWidget(self.open_folder_button)
        self.open_folder_button.clicked.connect(ActionSystem.open_folder)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setIcon(QtGui.QIcon("./assets/icons/save_file.svg"))
        self.save_button.setToolTip("Save File")
        self.tool_bar.addWidget(self.save_button)
        self.save_button.clicked.connect(ActionSystem.save_file)

        self.tool_bar.addSeparator()

        self.undo_button = QtWidgets.QPushButton()
        self.undo_button.setIcon(QtGui.QIcon("./assets/icons/undo.png"))
        self.undo_button.setToolTip("Undo")
        self.tool_bar.addWidget(self.undo_button)
        self.undo_button.clicked.connect(self.main_form.menu_bar.edit_menu_action_undo_callback)

        self.redo_button = QtWidgets.QPushButton()
        self.redo_button.setIcon(QtGui.QIcon("./assets/icons/redo.png"))
        self.redo_button.setToolTip("Redo")
        self.tool_bar.addWidget(self.redo_button)
        self.redo_button.clicked.connect(self.main_form.menu_bar.edit_menu_action_redo_callback)

        self.tool_bar.addSeparator()

        self.cut_button = QtWidgets.QPushButton()
        self.cut_button.setIcon(QtGui.QIcon("./assets/icons/cut.png"))
        self.cut_button.setToolTip("Cut")
        self.tool_bar.addWidget(self.cut_button)
        self.cut_button.clicked.connect(self.main_form.menu_bar.edit_menu_action_cut_callback)

        self.copy_button = QtWidgets.QPushButton()
        self.copy_button.setIcon(QtGui.QIcon("./assets/icons/copy.png"))
        self.copy_button.setToolTip("Cut")
        self.tool_bar.addWidget(self.copy_button)
        self.copy_button.clicked.connect(self.main_form.menu_bar.edit_menu_action_copy_callback)

        self.paste_button = QtWidgets.QPushButton()
        self.paste_button.setIcon(QtGui.QIcon("./assets/icons/paste.png"))
        self.paste_button.setToolTip("Paste")
        self.tool_bar.addWidget(self.paste_button)
        self.paste_button.clicked.connect(self.main_form.menu_bar.edit_menu_action_paste_callback)

        self.tool_bar.addSeparator()

        self.compiler_box = QtWidgets.QComboBox()
        self.compiler_box.setFixedHeight(27)
        self.compiler_box.setFixedWidth(120)
        self.compiler_box.addItem(QtGui.QIcon("./assets/logo/hacklogo.png"), "Hack Compiler")
        self.tool_bar.addWidget(self.compiler_box)

        self.compile_button = QtWidgets.QPushButton()
        self.compile_button.setIcon(QtGui.QIcon("./assets/icons/forward.png"))
        self.compile_button.setToolTip("Compile")
        self.tool_bar.addWidget(self.compile_button)
        self.compile_button.clicked.connect(ActionSystem.compile)

        self.comp_file_button = QtWidgets.QPushButton()
        self.comp_file_button.setIcon(QtGui.QIcon("./assets/icons/cmp.png"))
        self.comp_file_button.setToolTip("Load Comparison File")
        self.tool_bar.addWidget(self.comp_file_button)
        self.comp_file_button.clicked.connect(ActionSystem.load_comparison_file)

        self.cls_comp_file_button = QtWidgets.QPushButton()
        self.cls_comp_file_button.setIcon(QtGui.QIcon("./assets/icons/cls1.png"))
        self.cls_comp_file_button.setToolTip("Clear Comparison File")
        self.tool_bar.addWidget(self.cls_comp_file_button)
        self.cls_comp_file_button.clicked.connect(ActionSystem.clear_comparison_file)

        self.export_dest_button = QtWidgets.QPushButton()
        self.export_dest_button.setIcon(QtGui.QIcon("./assets/icons/save1.png"))
        self.export_dest_button.setToolTip("Save Destination To File")
        self.tool_bar.addWidget(self.export_dest_button)
        self.export_dest_button.clicked.connect(ActionSystem.export_destination)

        self.disable()

    def enable(self):
        """
        Enable buttons in tool bar.
        """
        self.cut_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.paste_button.setEnabled(True)
        self.undo_button.setEnabled(True)
        self.redo_button.setEnabled(True)
        self.compile_button.setEnabled(True)

    def disable(self):
        """
        Disable buttons in tool bar.
        """
        self.cut_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.paste_button.setEnabled(False)
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self.compile_button.setEnabled(False)