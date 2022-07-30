from math import floor
from pickle import TRUE
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

from PredefinedGuiElements.gameTile import gameTile

Letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

class Board:
    def __init__(self, gridLayout):
        self.Tiles = [[0 for x in range(10)] for y in range(10)] 

        #sets up boxes to contain tiles for ease of use
        self.BoxList = [[],[],[],[],[],[],[],[],[]]

        #populates the game grid with 100 tiles
        for x in range(10):
            for y in range(10):
                tile = gameTile(x, y, self)
                gridLayout.addWidget(tile, y , x)
                self.Tiles[x][y] = tile

        #organises tiles into boxes
        for x in range(1,10):
            for y in range(0,9):
                tile = self.Tiles[x][y]

                num = self.BoxNumberFromTile(tile.x, tile.y)
                self.BoxList[num].append(tile)

                #colour codes boxes for ease of strategy
                if ((num % 2) == 0):
                    tile.SetColour("darkGray")
                else:
                    tile.SetColour("lightGray")

        #sets up a coord system for easy reading of positions
        for x in range(10):
            self.Tiles[0][x].ChangeText(str(9-x))
            self.Tiles[0][x].SetColour("Gray")
            self.Tiles[0][x].SetStatic()
        for x in range(10):
            self.Tiles[x][9].ChangeText(Letters[x-1])
            self.Tiles[x][9].SetColour("Gray")
            self.Tiles[x][9].SetStatic()
        self.Tiles[0][9].ChangeText("")

        #defines a field for the number selected by the users
        self.selectedNumber = 0

    def setSelectedNumber(self, number):
        self.selectedNumber = number

    def tilePressed(self, x, y):
        #check that users have chosen a number to place
        if (self.selectedNumber == 0):
            return

        #checks if the tile can be played according to sodoku rules
        if ((not self.CheckRowValidity(y)) or (not self.CheckColumnValidity(x)) or (not self.CheckBoxValidity(x,y))):
            return
    
        #changes the tile
        self.Tiles[x][y].SetStatic()
        self.Tiles[x][y].SetNumber(self.selectedNumber)

    def CheckRowValidity(self, x):

        for j in range(1,10):  #for each tile in the row
            if (self.Tiles[j][x].GetText() != ""):  #if tile has a number on it
                if self.Tiles[j][x].GetNumber() == self.selectedNumber:  #if tile has the same number as the one trying to place
                    if (j != x):  #if tile isn't the one we're placing at
                        return False

        return True

    def CheckColumnValidity(self, y):
        for j in range(0,9):  #for each tile in the col
            if (self.Tiles[y][j].GetText() != ""):  #if tile has a number on it
                if self.Tiles[y][j].GetNumber() == self.selectedNumber:  #if tile has the same number as the one trying to place
                    if (y != j):  #if tile isn't the one we're placing at
                        return False

        return True

    def CheckBoxValidity(self, x, y):
        for tile in self.BoxList[self.BoxNumberFromTile(x, y)]:
            if (tile.GetText() != ""):
                if (tile.GetNumber() == self.selectedNumber):
                    if ((tile.x != x) and (tile.y != y)):
                        return False

        return True

    #takes a tile and from its x and y, returns what number box it belongs in (0-8)
    def BoxNumberFromTile(self, x, y): 
        x = x
        y = y + 1

        boxRow = floor((x-1)/3) 
        boxCol = floor((y-1)/3)       
        boxNum = boxCol*3 + boxRow

        return boxNum

