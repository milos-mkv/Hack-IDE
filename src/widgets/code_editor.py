"""
------------------------------------------------------------------------------
    @file       code_editor.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Code editor widget.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

from PyQt5                  import QtGui, QtCore, QtWidgets
from PyQt5.QtCore           import Qt, QRect, QSize
from PyQt5.QtWidgets        import QWidget, QPlainTextEdit, QTextEdit, QFrame, QShortcut
from PyQt5.QtGui            import QColor, QPainter, QTextFormat
from src.utils.asset_system import AssetSystem

class QLineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        self.setFont(AssetSystem.font)

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditorWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(AssetSystem.font)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        # self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.setTabStopDistance(4 * QtGui.QFontMetrics(AssetSystem.font).width(' '))
        self.updateLineNumberAreaWidth(0)
        self.setWordWrapMode(False)
        self.setStyleSheet("QPlainTextEdit:focus{border: none; outline: none; }")
        self.setStyleSheet("QPlainTextEdit{border: none; outline: none; selection-background-color: #F9A08D;}")
        # self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + QtGui.QFontMetrics(AssetSystem.font).width('9') * (digits + 1)
        return space

    def keyPressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Return:
            return
        super().keyPressEvent(event)
           

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth() + 20, 0, 0, 0) # + 20

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightLine(self, line):
        lineColor = QColor(Qt.green).lighter(160)

        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(lineColor)
        fmt.setProperty(QTextFormat.FullWidthSelection, True)

        block = self.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(fmt)

    def highlightComparisonLine1(self, line):
        lineColor = QColor(Qt.yellow).lighter(160)

        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(lineColor)
        fmt.setProperty(QTextFormat.FullWidthSelection, True)

        block = self.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(fmt)

    def highlightSuccLine(self, line):
        block = self.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)

        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.green).lighter(170)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = cursor
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def highlightErrorLine(self, line):
        block = self.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)

        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.red).lighter(170)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = cursor
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def highlightComparisonLine(self, line):
        block = self.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)

        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.yellow).lighter(130)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = cursor
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.green).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        # painter.fillRect(event.rect(), QColor(35,38,41))
        painter.fillRect(event.rect(), QColor(255, 255, 255))
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor(150, 150, 150))
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
                
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1