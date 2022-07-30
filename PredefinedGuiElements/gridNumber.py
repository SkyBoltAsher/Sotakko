from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class gridNumber(QLabel):
    def __init__(self, number, mainWindow):
        super().__init__()
        
        #formatting
        self.setText(str(number))
        self.setFont(QFont("Arial", 30))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("background-color: Gray")
        self.number = number

        #functionality
        self.mousePressEvent = self.OnClicked
        self.mainWindow = mainWindow

    def OnClicked(self, event):
        self.mainWindow.updateSelectedNumber(self.number)

    def SetColour(self, colour):
        self.setStyleSheet("background-color: " + colour)