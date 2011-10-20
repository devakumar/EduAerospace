import os
import platform
import sys
import re #Regular Expressions
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import qrc_resources
from ui import ui_mainwindow

__version__ = "1.0.0"

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
	""" """
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.filename = None
		self.setupUi(self)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	application = MainWindow()
	application.show()
	app.exec_()
