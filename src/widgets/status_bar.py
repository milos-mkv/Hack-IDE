"""
------------------------------------------------------------------------------
    @file       status_bar.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Status bar.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5 import QtWidgets, QtCore, QtGui

class StatusBarWidget(object):

    def __init__(self, main_form):
        """
        Constructs status bar widget.
        """
        self.main_form = main_form
        self.initialize_all_widgets()


    def initialize_all_widgets(self):
        """
        Initialize all widgets that exist in status bar widget.
        """
        self.status_bar = QtWidgets.QStatusBar()
        self.row_col_label = QtWidgets.QLabel()
        self.row_col_label.setText("   Ln: 0, Col: 0   ")
        self.status_bar.addWidget(self.row_col_label)
        self.main_form.setStatusBar(self.status_bar)
        self.hide()

    def update_line_and_col(self, line, col):
        """
        Update line and column in status bar.
        """
        self.row_col_label.setText("   Ln: {0}, Col: {1}   ".format(line, col))

    def hide(self):
        """ Hide status bar. """
        self.row_col_label.hide()

    def show(self):
        """ Show status bar. """
        self.row_col_label.show()