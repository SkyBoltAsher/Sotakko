from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

from PredefinedGuiElements.gameTile import gameTile

Letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

class Board:
    def __init__(self, gridLayout):
        self.Tiles = [[0 for x in range(10)] for y in range(10)] 

        #populates the game grid with 100 tiles
        for x in range(10):
            for y in range(10):
                tile = gameTile(x, y)
                gridLayout.addWidget(tile, y , x)
                self.Tiles[x][y] = tile

        for x in range(10):
            self.Tiles[0][x].ChangeText(str(x))
            