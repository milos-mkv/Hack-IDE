"""
------------------------------------------------------------------------------
    @file       about_window.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      About window.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class AboutDialog(QtWidgets.QDialog):

    def __init__(self, p):
        """ 
        Constructs about window. 
        """             
        QtWidgets.QDialog.__init__(self, p) 
        uic.loadUi("about.ui", self)          
        self.setWindowIcon(QtGui.QIcon("./assets/logo/hacklogo.png"))

    def keyPressEvent(self, event):
        """
        Key event for about window.
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()           