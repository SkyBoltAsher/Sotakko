from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class gameTile(QLabel):
    def __init__(self, x, y):
        super().__init__()
        
        self.setText("")
        self.x = x
        self.y = y
        self.setFont(QFont("Arial", 30))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("background-color: cyan")

    def SetNumber(self, x):
        self.setText(str(x))

    def GetNumber(self):
        return int(self.text)

    def ChangeText(self, text):
        self.setText(text)

    def SetColour(self, colour):
        self.setStyleSheet("background-color: " + colour)

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y