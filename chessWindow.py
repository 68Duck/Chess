from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class ChessWindow(QMainWindow,uic.loadUiType("chessWindow.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setupPieces()

    def initUI(self):
        self.squares = []
        startX = 50
        startY = 50
        width = 75
        height = 75
        for i in range(8):
            for j in range(8):
                self.createSquare(startX,startY,width,height,i,j)

    def setupPieces(self):
        for i in range(8):
            self.setSquarePiece(i*8+6,"pawnW")
            self.setSquarePiece(i*8+1,"pawnB")

        self.setSquarePiece(7,"rookW")
        self.setSquarePiece(63,"rookW")
        self.setSquarePiece(0,"rookB")
        self.setSquarePiece(56,"rookB")

        self.setSquarePiece(23,"bishopW")
        self.setSquarePiece(47,"bishopW")
        self.setSquarePiece(16,"bishopB")
        self.setSquarePiece(40,"bishopB")

        self.setSquarePiece(15,"knightW")
        self.setSquarePiece(55,"knightW")
        self.setSquarePiece(8,"knightB")
        self.setSquarePiece(48,"knightB")

        self.setSquarePiece(31,"kingW")
        self.setSquarePiece(24,"kingB")

        self.setSquarePiece(39,"queenW")
        self.setSquarePiece(32,"queenB")



    def setSquarePiece(self,squareNumber,pieceName): #square number is 0 indexed. Piece 0 is top left and moved down first
        pixmap = QPixmap(f"{pieceName}.png")
        self.squares[squareNumber].setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))

    def createSquare(self,startX,startY,width,height,x,y):
        self.newSquare = QLabel(self,alignment=Qt.AlignCenter)
        self.newSquare.setFixedSize(width,height)
        self.newSquare.move(startX+width*x,startY+height*y)
        if (x+y)%2==1:
            self.newSquare.setStyleSheet("background-color:#769656; border: 1px solid black;")
        else:
            self.newSquare.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
        self.squares.append(self.newSquare)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = ChessWindow()
    win.show()
    sys.exit(app.exec_())
