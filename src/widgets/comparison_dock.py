"""
------------------------------------------------------------------------------
    @file       comparison_dock.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Comparison dock.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5 import QtWidgets, QtCore, QtGui

class ComparisonDockWidget(object):

    def __init__(self, main_form):
        """
        Constructs comparison dock widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exist in comparison dock widget.
        """
        self.file   = None
        self.hidden = True
        self.dock   = QtWidgets.QDockWidget("Comparison", self.main_form)
        self.main_form.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)
        self.dock.visibilityChanged.connect(self.dock_visibilty_changed_callback)

        self.list = QtWidgets.QListWidget()
        self.list.setFont(QtGui.QFont("Consolas", 10))

        self.list.setStyleSheet("QListWidget { border: 1px solid lightgrey; }")
        self.dock.setWidget(self.list)
        self.hide()

    def show(self):
        """ Show comparison dock widget. """
        self.dock.show()

    def hide(self):
        """ Hide comparison dock widget. """
        self.dock.hide()

    def dock_visibilty_changed_callback(self, visible):
        """ Change visibility status of comarison dock widget. """
        self.hidden = not visible