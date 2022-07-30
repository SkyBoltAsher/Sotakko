from math import floor
import math
from pickle import TRUE
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from torch import AggregationType

from PredefinedGuiElements.gameTile import gameTile

Letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

class Board:
    def __init__(self, gridLayout, mainWindow):
        self.Tiles = [[0 for x in range(10)] for y in range(10)] 

        #records main window for function calls
        self.MainWindow = mainWindow

        #list of boxes that have been captured
        self.CapturesBoxes = []
        self.CapturingPlayers = []

        #sets up boxes to contain tiles for ease of use
        self.BoxList = [[],[],[],[],[],[],[],[],[]]

        #starts with a starting player
        self.currentPlayer = 1

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
        if ((not self.CheckRowValidity(y, self.selectedNumber)) or (not self.CheckColumnValidity(x, self.selectedNumber)) or (not self.CheckBoxValidity(x,y, self.selectedNumber))):
            return

          
    
        #changes the tile
        self.Tiles[x][y].SetStatic()
        self.Tiles[x][y].SetNumber(self.selectedNumber)

        #check if a tile has been captured
        self.CheckSodokuRule()  

        #check if the game has a winnder
        self.CheckTTTWin()
        
        #change the current player
        self.ChangeCurrentPlayer()

    def CheckRowValidity(self, x, checkedNumber):

        for j in range(1,10):  #for each tile in the row
            if (self.Tiles[j][x].GetText() != ""):  #if tile has a number on it
                if self.Tiles[j][x].GetNumber() == checkedNumber:  #if tile has the same number as the one trying to place
                    return False

        return True

    def CheckColumnValidity(self, y, checkedNumber):
        for j in range(0,9):  #for each tile in the col
            if (self.Tiles[y][j].GetText() != ""):  #if tile has a number on it
                if self.Tiles[y][j].GetNumber() == checkedNumber:  #if tile has the same number as the one trying to place
                    return False

        return True

    def CheckBoxValidity(self, x, y, checkedNumber):
        for tile in self.BoxList[self.BoxNumberFromTile(x, y)]:
            if (tile.GetText() != ""):
                if (tile.GetNumber() == checkedNumber):
                    if ((tile.x != x) or (tile.y != y)):
                        return False

        return True

    def CheckSodokuRule(self):
        for box in range(9): #for each box
            if (not (box in self.CapturesBoxes)):  #that has not been captured
                boxPossible = False
                for tile in self.BoxList[box]: #for each tile in that box
                    currentx = tile.x
                    currenty = tile.y

                    if (tile.static == False):  #if that tile is not static
                        for i in range(1,10):  #try each number
                            if (self.CheckRowValidity(currenty, i) and self.CheckColumnValidity(currentx, i) and self.CheckBoxValidity(currentx, currenty, i)):  #and see if it can be placed there
                                boxPossible = True

                if (boxPossible == False):  #if no possible moves within the box were found
                    self.CaptureBox(box)




    def CheckTTTWin(self):
        littleBoard = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]] 

        winner = -1   
        movecount = 0    

        #loads captured boxes into a box for easy analysis
        index = 0
        for x in range(3):
            for y in range(3):
                for j in range(len(self.CapturesBoxes)):
                    if (index == self.CapturesBoxes[j]):
                        movecount += 1
                        littleBoard[x][y] = self.CapturingPlayers[j]

                index = index + 1

        #check columns for win
        for k in range(3):
            if ((littleBoard[k][0] == littleBoard[k][1]) and (littleBoard[k][1] == littleBoard[k][2]) and (littleBoard[k][2] != -1)):
                winner = littleBoard[k][0]

        #check rows
        for p in range(3):
            if ((littleBoard[0][p] == littleBoard[1][p]) and (littleBoard[1][p] == littleBoard[2][p]) and (littleBoard[2][p] != -1)):
                winner = littleBoard[0][p]

        #check diagonals
        if ((littleBoard[0][0] == littleBoard[1][1]) and (littleBoard[1][1] == littleBoard[2][2]) and (littleBoard[2][2] != -1)):
            winner = littleBoard[0][0]
        if ((littleBoard[2][0] == littleBoard[1][1]) and (littleBoard[1][1] == littleBoard[0][2]) and (littleBoard[0][2] != -1)):
            winner = littleBoard[2][0]

        #check if a player won
        if (winner != -1):
            msg = QMessageBox()
            msg.setWindowTitle("Winner")
            if (winner == 1):
                msg.setText("Player 1 (X) has won!")
            else:
                msg.setText("Player 2 (0) has won!")

            msg.exec_()

            self.MainWindow.resetBoard()
        elif (movecount == (math.pow(3, 2) - 1)):
            msg = QMessageBox()
            msg.setWindowTitle("Tic Tac Toe is a stupid fucking game")
            msg.setText("It's actually ridiculous that people above the age of 5 would play such a dumb game. You can always force a draw! Fucking expression of skill right there 'oh ho ho look at me, im so good we will DRAW EVERYTIME'. God. Anyway, this game ended in a draw in case you didn't notice. Fuck me.")
            msg.exec_()
            self.MainWindow.resetBoard()




    def CaptureBox(self, box):
        if (self.currentPlayer == 1):
            self.BoxList[box][0].SetColour("Red")
            self.BoxList[box][2].SetColour("Red")
            self.BoxList[box][4].SetColour("Red")
            self.BoxList[box][6].SetColour("Red")
            self.BoxList[box][8].SetColour("Red")
        else:
            self.BoxList[box][0].SetColour("Blue")
            self.BoxList[box][1].SetColour("Blue")
            self.BoxList[box][2].SetColour("Blue")
            self.BoxList[box][3].SetColour("blue")
            self.BoxList[box][5].SetColour("blue")
            self.BoxList[box][6].SetColour("blue")
            self.BoxList[box][7].SetColour("blue")
            self.BoxList[box][8].SetColour("blue")

        self.CapturesBoxes.append(box)
        self.CapturingPlayers.append(self.currentPlayer)



    #takes a tile and from its x and y, returns what number box it belongs in (0-8)
    def BoxNumberFromTile(self, x, y): 
        x = x
        y = y + 1

        boxRow = floor((x-1)/3) 
        boxCol = floor((y-1)/3)       
        boxNum = boxCol*3 + boxRow

        return boxNum

    def ChangeCurrentPlayer(self):
        if (self.currentPlayer == 1):
            self.currentPlayer = 0
        else:
            self.currentPlayer = 1

        self.MainWindow.updateActivePlayerLabel(self.currentPlayer)