import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QFrame, QMenuBar, QVBoxLayout, QComboBox, QAction, QScrollArea)
from PyQt5.QtCore import Qt

from PredefinedGuiElements.gameTile import gameTile
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
        self.gameSeperationLayout.addWidget(self.gameGridWidget)  #locates the game grid to the left of the interfacing
        layout.addWidget(self.gameSeperationWidget)

        self.initGameGrid()
        
        #start the window
        self.show()

    def initGameGrid(self):

        self.gameBoard = Board(self.gameGridLayout)


app = QApplication(sys.argv) #all things need an application to start with
mainWindow = MainWindow()  #create an instance of the mainwindow class, which holds all other gui elements
sys.exit(app.exec_()) #this bit starts the application, with sys.exit used to cleanly close