"""
------------------------------------------------------------------------------
    @file       syntax_highlighter.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Syntax highlighter.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
import pygments, re
from pygments.lexers        import *
from pygments.token         import *
from pygments.lexer         import RegexLexer, include
from PyQt5                  import QtWidgets, QtCore, QtGui
from src.utils.asset_system import AssetSystem

class HackAssemblyLexer(RegexLexer):
    name      = 'Hack Assembler'
    aliases   = ['hack_asm']
    filenames = ['*.asm']

    identifier = r'[a-zA-Z$._?][a-zA-Z0-9$._?]*'

    flags = re.IGNORECASE | re.MULTILINE
    tokens = {
        'root': [
            include('whitespace'),
            (r'\(' + identifier + '\)', Name.Label),
            (r'[+-=;&|!]+', Operator),
            (r'\/\/.+$', Comment),
            (r'[\r\n]+', Text),
            (r'\b@(R0|R1|R2|R3|R4|R5|R6|R7|R8|R9|R10|R11|R12|R13|R14|R15)\b', Name.Builtin.Pseudo), # RAM Addresses
            (r'@[A-Za-z0-9.:$_]+', Name.Variable),
            (r'\b(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)\b', Keyword),
            (r'\b@(SCREEN|KBD)\b', Name.Builtin.Pseudo), # I/O addresses
            (r'\b@(SP|LCL|ARG|THIS|THAT)\b', Name.Builtin.Pseudo), # Parameter addresses
            (r'null', Keyword.Pseudo),
            (r'\b(D|M|MD|A|AM|AD|AMD)\b', Name.Builtin),
            (r'@[0-9]+', Name.Constant)
        ],
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'\/\/.*?\n', Comment),
            (r'#.*?\n', Comment)
        ]
    }

class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, document, file):
        """
        Constructs syntax highlighter.
        """
        QtGui.QSyntaxHighlighter.__init__(self, document)
        self.lexer = HackAssemblyLexer()
        
    def highlightBlock(self, text):
        try:
            index = 0
            for token, c in pygments.lex(text, self.lexer):
                try:
                    if token in AssetSystem.colors.keys():
                        _format = QtGui.QTextCharFormat()
                        _format.setForeground(AssetSystem.colors[token])
                        self.setFormat(index, len(c), _format)
                    index += len(c)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)