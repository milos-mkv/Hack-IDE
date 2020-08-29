"""
------------------------------------------------------------------------------
    @file       tab_bar.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Tab bar.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5                          import QtWidgets, QtCore, QtGui
from src.utils.log_system           import LogSystem
from src.utils.action_system        import ActionSystem
from src.utils.asset_system         import AssetSystem
from src.widgets.code_editor        import CodeEditorWidget
from src.widgets.syntax_highlighter import SyntaxHighlighter

class TabStruct(object):

    main_form = None  # Our main form application

    def __init__(self):
        self.widget    = QtWidgets.QWidget()   # This is the tab widget
        self.textarea  = CodeEditorWidget()    # Code editor in tab widget
        self.syntax    = None                  # Syntax highlighter for code editor
        self.saved     = False                 # Save status for code editor
        self.title     = "untitled"            # Title of tab
        self.file_path = None                  # File path
        self.initialize_all_widgets()          # Initialize all widgets

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exits in tab.
        """
        self.widget.layout = QtWidgets.QHBoxLayout(self.widget) # Set layout for widget
        self.widget.layout.addWidget(self.textarea)             # Add code editor to layout
        self.textarea.cursorPositionChanged.connect(self.textarea_cursor_change_callback)
        self.textarea.textChanged.connect(self.textarea_text_changed_callback)

    def textarea_cursor_change_callback(self):
        """
        Text area cursor chage callback function.
        """
        row = self.textarea.textCursor().blockNumber() + 1
        col = self.textarea.textCursor().columnNumber() + 1
        TabStruct.main_form.status_bar.update_line_and_col(row, col)

    def textarea_text_changed_callback(self):
        """
        Text area text chage callback function.
        """
        if self.saved:
            self.saved = False
            self.textarea.setExtraSelections([])

    def apply_new_font(self, font):
        """
        Apply new font to code editor in tab.
        """
        self.textarea.setFont(font)
        self.textarea.lineNumberArea.setFont(font)
        self.textarea.setTabStopDistance(4 * QtGui.QFontMetrics(font).width(' '))

class TabBarWidget(object):

    def __init__(self, main_form):
        """
        Constructs tab bar widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets() 

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exist in tab bar widget.
        """
        self.tab_bar = self.main_form.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.tab_bar.hide()
        self.tab_bar.tabCloseRequested.connect(self.tab_bar_close_tab_request_callback)
        self.tab_bar.currentChanged.connect(self.tab_bar_current_tab_changed_callback)
        
        self.current_index = 0
        self.hidden_tabs   = False
        self.tabs          = []

        # Label that will show when there are no tabs opened
        self.hidden_label = QtWidgets.QLabel()
        self.hidden_label.setText("Ctrl + N to create new file")
        self.hidden_label.setAlignment(QtCore.Qt.AlignCenter)

        palette_for_label = QtGui.QPalette()
        palette_for_label.setColor(self.hidden_label.foregroundRole(), QtGui.QColor(150, 150, 150))
        self.hidden_label.setPalette(palette_for_label)
        self.main_form.central_widget.layout().addWidget(self.hidden_label)

        TabStruct.main_form = self.main_form

    def tab_bar_close_tab_request_callback(self, source):
        """
        Remove requested tab from list of opened tabs.
        """
        widget = self.tab_bar.widget(source)
        for tab in self.tabs:
            if tab.widget == widget:
                LogSystem.warning("Removing requested tab! [Index {0}]".format(self.tabs.index(tab)))
                self.tabs.remove(tab)
                break

        widget.deleteLater()
        self.tab_bar.removeTab(source)  # Remove tab from list of tabs

        # Check if list of opened tab is empty, and if it is hide and show some widgets
        if len(self.tabs) == 0:
            self.tab_bar.hide()
            self.hidden_label.show()
            self.main_form.status_bar.hide()
            self.main_form.tool_bar.disable()
            self.main_form.menu_bar.run_menu_action_compile.setEnabled(False)

    def tab_bar_current_tab_changed_callback(self, source):
        """
        Change index of currently selected tab.
        """
        widget = self.tab_bar.widget(source)
        for tab in self.tabs:
            if tab.widget == widget:
                self.current_index = self.tabs.index(tab)
                self.tabs[self.current_index].textarea_cursor_change_callback()
                LogSystem.information("Current tab in focus! [Index {0}]".format(self.current_index))
                break

    def create_new_tab(self, file_path=None):
        """
        Create new tab.
        """
        if len(self.tabs) == 0:
            self.tab_bar.show()
            self.hidden_label.hide()
            self.main_form.status_bar.show()
            self.main_form.tool_bar.enable()
            self.main_form.menu_bar.run_menu_action_compile.setEnabled(True)

        # Check if file path is provided
        if file_path:   
            for tab in self.tabs:
                # Check if we have that file opened in some tab
                if tab.file_path == file_path:  
                    # If we have set focus on it
                    self.tab_bar.setCurrentWidget(tab.widget)
                    tab.textarea.setFocus()
                    return

        self.tabs.append(TabStruct())
        self.tabs[-1].file_path = file_path

        if file_path:
            self.tabs[-1].title     = file_path.split("/")[-1]
            self.tabs[-1].extension = file_path.split(".")[-1]

            try:
                # Set syntax highlighter
                if self.tabs[-1].extension == "asm":
                    self.tabs[-1].syntax = SyntaxHighlighter(self.tabs[-1].textarea.document(), file_path)
            except Exception as e:
                LogSystem.error(e)

            # Read text from file
            try:
                with open(file_path, "r", errors="ignore") as file:
                    text_buffer = file.read()
                    self.tabs[-1].textarea.setPlainText(text_buffer)
            except Exception as e:
                LogSystem.error(e)

        self.tab_bar.addTab(self.tabs[-1].widget, self.tabs[-1].title)
        self.tab_bar.setCurrentWidget(self.tabs[-1].widget)
        self.tab_bar.setTabIcon(len(self.tabs) - 1, AssetSystem.icons["FILE"])
        self.tabs[-1].textarea.setFocus()

    def remove(self, tab):
        """
        Remove tab.
        """
        index = self.tab_bar.indexOf(tab.widget)
        self.tab_bar_close_tab_request_callback(index)

    # Getter for current tab in focus
    @property
    def current(self): return self.tabs[self.current_index]
    
    @property
    def get(self): return self.tab_bar