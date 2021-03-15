from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class ChessWindow(QMainWindow,uic.loadUiType("chessWindow.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.squares = []
        startX = 50
        startY = 50
        width = 75
        height = 75
        for i in range(8):
            for j in range(8):
                self.createSquare(startX,startY,width,height,i,j)

    def createSquare(self,startX,startY,width,height,x,y):
        self.newSquare = QLabel(self,alignment=Qt.AlignCenter)
        self.newSquare.setFixedSize(width,height)
        self.newSquare.move(startX+width*x,startY+height*y)
        if (x+y)%2==1:
            self.newSquare.setStyleSheet("background-color:#769656; border: 1px solid black;")
        else:
            self.newSquare.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
        pixmap = QPixmap("pawnW.png")
        # pixmap = pixmap.scaledToWidth(64)
        # pixmap = pixmap.scaledToHeight(64)
        self.newSquare.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = ChessWindow()
    win.show()
    sys.exit(app.exec_())
