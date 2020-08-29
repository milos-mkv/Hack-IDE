"""
------------------------------------------------------------------------------
    @file       compilation_dock.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Compilation dock.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5 import QtWidgets, QtCore, QtGui

class CompilationDockWidget(object):

    def __init__(self, main_form):
        """
        Constructs compilation dock widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """ 
        Initialize all widgets that exist in compilation dock widget.
        """
        self.hidden = True
        self.dock   = QtWidgets.QDockWidget("Compilation information", self.main_form)
        self.main_form.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock)
        self.dock.visibilityChanged.connect(self.dock_visibilty_changed_callback)

        self.textarea = QtWidgets.QPlainTextEdit()
        self.textarea.setReadOnly(True)
        self.textarea.setFont(QtGui.QFont("Consolas", 12))
        self.textarea.setMaximumHeight(120)

        self.textarea.setStyleSheet("QPlainTextEdit { border: 1px solid lightgrey; }")
        self.dock.setWidget(self.textarea)
        self.hide()

    def show(self):
        """ Show compilation dock widget. """
        self.dock.show()

    def hide(self):
        """ Hide compilation dock widget. """
        self.dock.hide()

    def dock_visibilty_changed_callback(self, visible):
        """ Change visibility status of compilation dock widget. """
        self.hidden = not visible