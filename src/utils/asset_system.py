"""
------------------------------------------------------------------------------
    @file       asset_system.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Asset system for IDE.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

from PyQt5          import QtGui
from pygments.token import Token
import json

class AssetSystem(object):

    icons = {}

    @classmethod
    def initialize(cls):
        """ Initialize asset system. """
        cls.font = None
        try:
            with open("settings.json", "r") as settings_file:
                data = json.load(settings_file)
                cls.font = QtGui.QFont(data["FontFamily"], data["FontSize"], data["FontWeight"])
        except Exception as e:
            with open("settings.json", "w") as settings_file:
                data = {"FontFamily": "Consolas", "FontSize": 12, "FontWeight": 75 }
                cls.font = QtGui.QFont(data["FontFamily"], data["FontSize"], data["FontWeight"])
                json.dump(data, settings_file)

        cls.icons["DIR"]  = QtGui.QIcon("assets/icons/folder.svg")
        cls.icons["FILE"] = QtGui.QIcon("assets/icons/file.svg")

        cls.colors = {
            Token.Name.Variable:        QtGui.QColor(  0,   0, 255),
            Token.Comment:              QtGui.QColor(150, 150, 150),
            Token.Name.Label:           QtGui.QColor(255, 100, 100),
            Token.Keyword:              QtGui.QColor(100, 100, 255),
            Token.Name.Builtin.Pseudo:  QtGui.QColor(255, 255,   0),
            Token.Name.Constant:        QtGui.QColor(255,   0, 255),
        }