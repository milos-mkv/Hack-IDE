"""
------------------------------------------------------------------------------
    @file       menu_bar.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Find dock.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5                   import QtWidgets, QtCore, QtGui
from src.utils.log_system    import LogSystem
from src.utils.action_system import ActionSystem
from src.utils.asset_system  import AssetSystem
import json

class MenuBarWidget(object):

    def __init__(self, main_form):
        """
        Constructs menu bar widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exits in menu bar widget.
        """
        LogSystem.information("Initializing all menu widgets")
        self.file_menu_action_new_file     = self.main_form.findChild(QtWidgets.QAction, "actionNew_File")
        self.file_menu_action_open_file    = self.main_form.findChild(QtWidgets.QAction, "actionOpen_File")
        self.file_menu_action_open_folder  = self.main_form.findChild(QtWidgets.QAction, "actionOpen_Folder")
        self.file_menu_action_save_file    = self.main_form.findChild(QtWidgets.QAction, "actionSave_File")
        self.file_menu_action_save_file_as = self.main_form.findChild(QtWidgets.QAction, "actionSave_File_As")
        self.file_menu_action_exit         = self.main_form.findChild(QtWidgets.QAction, "actionExit")

        self.file_menu_action_new_file.triggered.connect(self.file_menu_action_new_file_callback)
        self.file_menu_action_open_file.triggered.connect(self.file_menu_action_open_file_callback)
        self.file_menu_action_open_folder.triggered.connect(self.file_menu_action_open_folder_callback)
        self.file_menu_action_save_file.triggered.connect(self.file_menu_action_save_file_callback)
        self.file_menu_action_save_file_as.triggered.connect(self.file_menu_action_save_file_as_callback)
        self.file_menu_action_exit.triggered.connect(self.file_menu_action_exit_callback)

        self.edit_menu_action_undo  = self.main_form.findChild(QtWidgets.QAction, "actionUndo")
        self.edit_menu_action_redo  = self.main_form.findChild(QtWidgets.QAction, "actionRedo")
        self.edit_menu_action_cut   = self.main_form.findChild(QtWidgets.QAction, "actionCut")
        self.edit_menu_action_copy  = self.main_form.findChild(QtWidgets.QAction, "actionCopy")
        self.edit_menu_action_paste = self.main_form.findChild(QtWidgets.QAction, "actionPaste")
        self.edit_menu_action_find  = self.main_form.findChild(QtWidgets.QAction, "actionFind")

        self.edit_menu_action_undo.triggered.connect(self.edit_menu_action_undo_callback)
        self.edit_menu_action_redo.triggered.connect(self.edit_menu_action_redo_callback)
        self.edit_menu_action_cut.triggered.connect(self.edit_menu_action_cut_callback)
        self.edit_menu_action_copy.triggered.connect(self.edit_menu_action_copy_callback)
        self.edit_menu_action_paste.triggered.connect(self.edit_menu_action_paste_callback)
        self.edit_menu_action_find.triggered.connect(self.edit_menu_action_find_callback)

        self.view_menu_action_toggle_dir_view         = self.main_form.findChild(QtWidgets.QAction, "actionToggle_Directory_View")
        self.view_menu_action_toggle_tabs             = self.main_form.findChild(QtWidgets.QAction, "actionToggle_Tabs")
        self.view_menu_action_toggle_toolbar          = self.main_form.findChild(QtWidgets.QAction, "actionToggle_Toolbar")
        self.view_menu_action_toggle_destination_dock = self.main_form.findChild(QtWidgets.QAction, "actionToggle_Destination_Dock")
        self.view_menu_action_toggle_comparison_dock  = self.main_form.findChild(QtWidgets.QAction, "actionToggle_Comparison_Dock")

        self.view_menu_action_toggle_dir_view.triggered.connect(self.view_menu_action_toggle_dir_view_callback)
        self.view_menu_action_toggle_tabs.triggered.connect(self.view_menu_action_toggle_tabs_callback)
        self.view_menu_action_toggle_toolbar.triggered.connect(self.view_menu_action_toggle_toolbar_callback)
        self.view_menu_action_toggle_destination_dock.triggered.connect(self.view_menu_action_toggle_destination_dock_callback)
        self.view_menu_action_toggle_comparison_dock.triggered.connect(self.view_menu_action_toggle_comparison_dock_callback)

        self.run_menu_action_compile           = self.main_form.findChild(QtWidgets.QAction, "actionCompile")
        self.run_menu_action_load_cmp_file     = self.main_form.findChild(QtWidgets.QAction, "actionLoad_Comparison_File")
        self.run_menu_action_cls_cmp_file      = self.main_form.findChild(QtWidgets.QAction, "actionClear_Comparison_File")
        self.run_menu_action_save_dest_to_file = self.main_form.findChild(QtWidgets.QAction, "actionSave_Destination_To_File")

        self.run_menu_action_compile.setEnabled(False)

        self.run_menu_action_compile.triggered.connect(self.run_menu_action_compile_callback)
        self.run_menu_action_load_cmp_file.triggered.connect(self.run_menu_action_load_cmp_file_callback)
        self.run_menu_action_cls_cmp_file.triggered.connect(self.run_menu_action_cls_cmp_file_callback)
        self.run_menu_action_save_dest_to_file.triggered.connect(self.run_menu_action_save_dest_to_file_callback)

        self.help_menu_action_about    = self.main_form.findChild(QtWidgets.QAction, "actionAbout")
        self.settings_menu_action_font = self.main_form.findChild(QtWidgets.QAction, "actionFont")

        self.help_menu_action_about.triggered.connect(self.help_menu_action_about_callback)
        self.settings_menu_action_font.triggered.connect(self.settings_menu_action_font_callback)

    def file_menu_action_new_file_callback(self):
        """
        File menu action new file callback.
        """
        LogSystem.information("File menu: New File")
        ActionSystem.new_file()

    def file_menu_action_open_file_callback(self):
        """
        File menu action open file callback.
        """
        LogSystem.information("File menu: Open File")
        ActionSystem.open_file()

    def file_menu_action_open_folder_callback(self):
        """
        File menu action open folder callback.
        """
        LogSystem.information("File menu: Open Folder")
        ActionSystem.open_folder()

    def file_menu_action_save_file_callback(self):
        """
        File menu action save file callback.
        """
        LogSystem.information("File menu: Save File")
        ActionSystem.save_file()

    def file_menu_action_save_file_as_callback(self):
        """
        File menu action save file as callback.
        """
        LogSystem.information("File menu: Save File As")
        ActionSystem.save_file_as()

    def file_menu_action_exit_callback(self):
        """
        File menu action exit callback.
        """
        LogSystem.information("File menu: Exit")
        QtWidgets.QApplication.instance().quit()

    def edit_menu_action_undo_callback(self):
        """
        Edit menu action undo callback.
        """
        LogSystem.information("Edit menu: Undo")
        try:
            self.main_form.tab_bar.current.textarea.undo()
        except Exception as e:
            LogSystem.error(e)

    def edit_menu_action_redo_callback(self):
        """
        Edit menu action redo callback.
        """
        LogSystem.information("Edit menu: Redo")
        try:
            self.main_form.tab_bar.current.textarea.redo()
        except Exception as e:
            LogSystem.error(e)

    def edit_menu_action_cut_callback(self):
        """
        Edit menu action cut callback.
        """
        LogSystem.information("Edit menu: Cut")
        try:
            self.main_form.tab_bar.current.textarea.cut()
        except Exception as e:
            LogSystem.error(e)

    def edit_menu_action_copy_callback(self):
        """
        Edit menu action copy callback.
        """
        LogSystem.information("Edit menu: Copy")
        try:
            self.main_form.tab_bar.current.textarea.copy()
        except Exception as e:
            LogSystem.error(e)

    def edit_menu_action_paste_callback(self):
        """
        Edit menu action paste callback.
        """
        LogSystem.information("Edit menu: Paste")
        try:
            self.main_form.tab_bar.current.textarea.paste()
        except Exception as e:
            LogSystem.error(e)

    def edit_menu_action_find_callback(self):
        """
        Edit menu action find callback.
        """
        LogSystem.information("Edit menu: Find")
        self.main_form.find_dock.show()

    def view_menu_action_toggle_dir_view_callback(self):
        """
        View menu action toggle directory view callback.
        """
        LogSystem.information("View menu: Toggle Directory View")

        if self.main_form.directory_view.hidden:
            self.main_form.directory_view.dock.show()
        else:
            self.main_form.directory_view.dock.hide()
        
    def view_menu_action_toggle_tabs_callback(self):
        """
        View menu action toggle tabs callback.
        """
        LogSystem.information("View menu: Toggle Tabs")

        if self.main_form.tab_bar.hidden_tabs:
            self.main_form.tab_bar.get.tabBar().show()
            self.main_form.tab_bar.hidden_tabs = False
        else:
            self.main_form.tab_bar.get.tabBar().hide()
            self.main_form.tab_bar.hidden_tabs = True

    def view_menu_action_toggle_toolbar_callback(self):
        """
        View menu action toggle toolbar callback.
        """
        LogSystem.information("View menu: Toggle Toolbar")
        if self.main_form.tool_bar.hidden:
            self.main_form.tool_bar.tool_bar.show()
            self.main_form.tool_bar.hidden = False
        else:
            self.main_form.tool_bar.tool_bar.hide()
            self.main_form.tool_bar.hidden = True

    def view_menu_action_toggle_destination_dock_callback(self):
        """
        View menu action toggle destination dock callback.
        """
        LogSystem.information("View menu: Toggle Destination Dock")
        if self.main_form.destination_dock.hidden:
            self.main_form.destination_dock.dock.show()
        else:
            self.main_form.destination_dock.dock.hide()

    def view_menu_action_toggle_comparison_dock_callback(self):
        """
        View menu action toggle comparison dock callback.
        """
        LogSystem.information("View menu: Toggle Comparison Dock")
        if self.main_form.comparison_dock.hidden:
            self.main_form.comparison_dock.dock.show()
        else:
            self.main_form.comparison_dock.dock.hide()

    def run_menu_action_compile_callback(self):
        """
        Run menu action compile callback.
        """
        LogSystem.information("Run menu: Compile")
        ActionSystem.compile()

    def run_menu_action_load_cmp_file_callback(self):
        """
        Run menu action load comparison file callback.
        """
        LogSystem.information("Run menu: Load Comparison File")
        ActionSystem.load_comparison_file()

    def run_menu_action_cls_cmp_file_callback(self):
        """
        Run menu action clear comparison file callback.
        """
        LogSystem.information("Run menu: Clear Comparison File")
        ActionSystem.clear_comparison_file()

    def run_menu_action_save_dest_to_file_callback(self):
        """
        Run menu action save destination to file callback.
        """
        LogSystem.information("Run menu: Save Destination To File")
        ActionSystem.export_destination()

    def settings_menu_action_font_callback(self):
        """
        Settings menu action font callback.
        """
        try:
            font, ok = QtWidgets.QFontDialog.getFont()
            if ok:
                font_family = font.family()
                font_size = font.pointSize()
                font_weight = font.weight()
                data = {
                    "FontFamily": font_family,
                    "FontSize":   font_size,
                    "FontWeight": font_weight
                }
                AssetSystem.font = QtGui.QFont(font_family, font_size, font_weight)
                for tab in self.main_form.tab_bar.tabs:
                    tab.apply_new_font(AssetSystem.font)

                with open("settings.json", "w") as settings_file:
                    json.dump(data, settings_file)

        except Exception as e:
            LogSystem.error(e)

    def help_menu_action_about_callback(self):
        """
        Help menu action about callback.
        """
        self.main_form.about_dialog.show()