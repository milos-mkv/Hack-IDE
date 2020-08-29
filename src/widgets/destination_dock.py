"""
------------------------------------------------------------------------------
    @file       destination_dock.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Destination dock.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5 import QtWidgets, QtCore, QtGui

class DestinationDockWidget(object):

    def __init__(self, main_form):
        """
        Constructs destination dock.
        """
        self.main_form = main_form
        self.initialize_all_widgets()

    def initialize_all_widgets(self):
        """
        Initialize all widgets that exist in destination dock widget.
        """
        self.pc        = None
        self.file_path = None
        self.hidden    = True
        self.dock = QtWidgets.QDockWidget("Destination", self.main_form)
        self.main_form.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)
        self.dock.visibilityChanged.connect(self.dock_visibilty_changed_callback)

        self.list = QtWidgets.QListWidget()
        self.list.setFont(QtGui.QFont("Consolas", 10))

        self.list.setStyleSheet("QListWidget { border: 1px solid lightgrey; }")
        self.list.itemClicked.connect(self.item_clicked_callback)
        self.dock.setWidget(self.list)
        self.hide()

    def item_clicked_callback(self, item):
        """
        Destination dock item click callback function.
        """
        try:
            if self.main_form.tab_bar.current.file_path != self.file_path:
                return
            index = self.list.indexFromItem(item).row()
            line  = self.pc[index]
            self.main_form.tab_bar.current.textarea.highlightSuccLine(line - 1)
        except Exception as e:
            print(e)

    def show(self):
        """ Show destination dock widget. """
        self.dock.show()

    def hide(self):
        """ Hide destination dock widget. """
        self.dock.hide()

    def dock_visibilty_changed_callback(self, visible):
        """ Change visibility status of destination dock widget. """
        self.hidden = not visible