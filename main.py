import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtCore import Qt

from PredefinedGuiElements.gameTile import gameTile
from PredefinedGuiElements.gridNumber import gridNumber
from NonGuiDataStructures.Board import Board



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sotakko")
        self.move(600,400) #position on screen that window is created
        self.resize(1000,600) #size of window when it's created

        #defines the largest layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  #makes it so layout touches edges of window
        self.setLayout(layout)

        #defines two layouts to use in structuring the game window
        self.gameSeperationLayout = QHBoxLayout() #the layout that contains the game grid on the left, and the options and interfacing on the right
        self.gameSeperationWidget = QWidget()
        self.gameSeperationWidget.setLayout(self.gameSeperationLayout)
        self.gameGridLayout = QGridLayout() #the layout that contains each of the 81 squares in sotakko
        self.gameGridWidget = QWidget()  #widget to hole the grid layout
        self.gameGridWidget.setLayout(self.gameGridLayout) #puts the grid layout in the grid widget
        self.gameSeperationLayout.addWidget(self.gameGridWidget, stretch=2)  #locates the game grid to the left of the interfacing
        layout.addWidget(self.gameSeperationWidget)

        #creates the game grid
        self.initGameGrid()

        #creates the interfacing section
        self.initInterfacing()
        
        #start the window
        self.show()

    def initGameGrid(self):

        self.gameBoard = Board(self.gameGridLayout)

    def initInterfacing(self):

        #layout connecting
        self.interfaceWidget = QWidget()
        self.interfaceLayout = QVBoxLayout()
        self.interfaceWidget.setLayout(self.interfaceLayout)
        self.gameSeperationLayout.addWidget(self.interfaceWidget, stretch=1)

        self.numberGridLayout = QGridLayout()
        self.numberGridWidget = QWidget()
        self.numberGridWidget.setLayout(self.numberGridLayout)
        self.interfaceLayout.addWidget(self.numberGridWidget)

        #adding number widgets
        self.gridNumbers = []
        tile = gridNumber(1, self)
        self.numberGridLayout.addWidget(tile, 0, 0)
        self.gridNumbers.append(tile)
        tile = gridNumber(2, self)
        self.numberGridLayout.addWidget(tile, 0, 1)
        self.gridNumbers.append(tile)
        tile = gridNumber(3, self)
        self.numberGridLayout.addWidget(tile, 0, 2)
        self.gridNumbers.append(tile)
        tile = gridNumber(4, self)
        self.numberGridLayout.addWidget(tile, 1, 0)
        self.gridNumbers.append(tile)
        tile = gridNumber(5, self)
        self.numberGridLayout.addWidget(tile, 1, 1)
        self.gridNumbers.append(tile)
        tile = gridNumber(6, self)
        self.numberGridLayout.addWidget(tile, 1, 2)
        self.gridNumbers.append(tile)
        tile = gridNumber(7, self)
        self.numberGridLayout.addWidget(tile, 2, 0)
        self.gridNumbers.append(tile)
        tile = gridNumber(8, self)
        self.numberGridLayout.addWidget(tile, 2, 1)
        self.gridNumbers.append(tile)
        tile = gridNumber(9, self)
        self.numberGridLayout.addWidget(tile, 2, 2)
        self.gridNumbers.append(tile)


    #updates the boards selected number
    def updateSelectedNumber(self, number):
        for x in self.gridNumbers:
            x.SetColour("Gray")
        self.gridNumbers[number - 1].SetColour("green")

        self.gameBoard.setSelectedNumber(number)




app = QApplication(sys.argv) #all things need an application to start with
mainWindow = MainWindow()  #create an instance of the mainwindow class, which holds all other gui elements
sys.exit(app.exec_()) #this bit starts the application, with sys.exit used to cleanly close