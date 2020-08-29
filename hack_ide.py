"""
------------------------------------------------------------------------------
    @file       hack_ide.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Integrated development environment for hack.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

import sys, time
from PyQt5                        import QtWidgets, QtGui, QtCore, uic
from src.utils.log_system         import LogSystem
from src.utils.action_system      import ActionSystem
from src.utils.asset_system       import AssetSystem
from src.widgets.menu_bar         import MenuBarWidget
from src.widgets.directory_view   import DirectoryViewWidget
from src.widgets.tab_bar          import TabBarWidget
from src.widgets.status_bar       import StatusBarWidget
from src.widgets.find_dock        import FindDockWidget
from src.widgets.tool_bar         import ToolBarWidget
from src.widgets.destination_dock import DestinationDockWidget
from src.widgets.comparison_dock  import ComparisonDockWidget
from src.widgets.compilation_dock import CompilationDockWidget
from src.widgets.about_window     import AboutDialog

class HackIDE(QtWidgets.QMainWindow):

    def __init__(self):      
        """
        Constructs hack integrated development environment form.
        """
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("form.ui", self)          # Load existing form design.
        self.initialize_all_widgets()        # Initialize all widgets in main window.
        self.setWindowIcon(QtGui.QIcon("./assets/logo/hacklogo.png"))
        self.setWindowTitle("Hack IDE")
        self.resize(800, 500)                # Set starting window size on 800 x 500.
        self.show()                          # Show window.

    def initialize_all_widgets(self):
        """ 
        Initialize all widgets that exist in main window 
        """
        LogSystem.initialize()
        LogSystem.information("Starting main window widgets initialization!")

        ActionSystem.initialize(self)           # Initialize actions for our main window.
        AssetSystem.initialize()                # Initialize assets.

        self.central_widget   = self.findChild(QtWidgets.QWidget, "centralwidget")
        self.about_dialog     = AboutDialog(self)
        self.menu_bar         = MenuBarWidget(self)          # Initialize menu bar custom widget.
        self.directory_view   = DirectoryViewWidget(self)    # Initialize directory view custom widget.
        self.tab_bar          = TabBarWidget(self)           # Initialize tab bar custom widget.
        self.status_bar       = StatusBarWidget(self)        # Initialize status bar custom widget.
        self.find_dock        = FindDockWidget(self)         # Initialize find dock custom widget.
        self.tool_bar         = ToolBarWidget(self)          # Initialize tool bar custom widget.
        self.destination_dock = DestinationDockWidget(self)  # Initialize destination dock custom widget.
        self.comparison_dock  = ComparisonDockWidget(self)   # Initialize comparison dock custom widget.
        self.compilation_dock = CompilationDockWidget(self)  # Initialize compilation docck custom widget.

    def keyPressEvent(self, event):
        """
        Key press event for main window.
        """
        if event.key() == QtCore.Qt.Key_Escape: # If we hit ECS
            self.find_dock.hide()               # Hide find dock widget
            self.about_dialog.hide()

if __name__ == "__main__":

    application = QtWidgets.QApplication(sys.argv)

    splash_pix = QtGui.QPixmap("./assets/logo/splash.png")
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)
    splash.show()

    application.processEvents()
    time.sleep(3)

    hack_ide = HackIDE()
    splash.finish(hack_ide)
    sys.exit(application.exec_())