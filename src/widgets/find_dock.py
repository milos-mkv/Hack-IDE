"""
------------------------------------------------------------------------------
    @file       find_dock.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Find dock.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5                import QtWidgets, QtCore, QtGui
from src.utils.log_system import LogSystem

class FindDockWidget(object):

    def __init__(self, main_form):
        """
        Constructs find dock widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exit in find dock.
        """
        self.find_dock_window = QtWidgets.QDockWidget("Find", self.main_form)
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Serach for...")
        self.input.setStyleSheet("QLineEdit{border: 1px solid lightgrey; padding-left: 5px;padding-top: 3px; padding-bottom: 3px; }")
        self.input.returnPressed.connect(self.input_callback)

        self.find_dock_window.setWidget(self.input)
        self.main_form.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.find_dock_window)
        self.find_dock_window.hide()

    def show(self):
        """ Show find dock widget. """
        self.find_dock_window.show()
        self.input.setFocus()

    def hide(self):
        """ Hide find dock widget. """
        self.find_dock_window.hide()
        self.input.clearFocus()
        self.input.clear()

    def input_callback(self):
        """ Input callback for find dock widget. """
        text = self.input.text()
        if not text:
            return
        try:
            if not self.main_form.tab_bar.current.textarea.find(text):
                cursor = self.main_form.tab_bar.current.textarea.textCursor()
                cursor.setPosition(0)
                self.main_form.tab_bar.current.textarea.setTextCursor(cursor)
                self.input_callback()
        except Exception as e:
            LogSystem.error(e)  
