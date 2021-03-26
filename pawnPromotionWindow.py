from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*


class PawnPromotionWindow(QMainWindow,uic.loadUiType("pawnPromotion.ui")[0]):
    def __init__(self,pieceColour,parentWindow,squareNumber):
        super().__init__()
        self.squareNumber = squareNumber
        self.parentWindow = parentWindow
        self.pieceColour = pieceColour
        self.setupUi(self)
        self.initUI()
        self.show()


    def initUI(self):
        self.setWindowTitle("Choose Piece")
        self.pieces = []
        if self.pieceColour == "white":
            colour = "W"
        else:
            colour = "B"
        self.createPiece(50,50,100,100,f"queen{colour}")
        self.createPiece(175,50,100,100,f"rook{colour}")
        self.createPiece(300,50,100,100,f"bishop{colour}")
        self.createPiece(425,50,100,100,f"knight{colour}")

    def createPiece(self,x,y,width,height,pieceName):
        self.newPiece = QLabel(self,alignment=Qt.AlignCenter)
        self.newPiece.setFixedSize(width,height)
        self.newPiece.move(x,y)
        self.newPiece.pieceName = pieceName
        self.newPiece.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
        pixmap = QPixmap(f"{pieceName}.png")
        self.newPiece.setPixmap(pixmap.scaled(width,height,Qt.KeepAspectRatio))
        self.pieces.append(self.newPiece)

    def pieceClicked(self,piece):
        if self.parentWindow is not None:
            self.parentWindow.promotedOptionChosen(piece.pieceName,self.squareNumber)
        else:
            print(piece.pieceName)
        self.close()


    def mousePressEvent(self,e):
        x = e.x()
        y = e.y()
        for piece in self.pieces:
            width = piece.width()
            height = piece.height()
            xpos = piece.x()
            ypos = piece.y()
            if x > xpos and x < xpos + width:
                if y > ypos and y < ypos + height:
                    self.pieceClicked(piece)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = PawnPromotionWindow("black",None)
    win.show()
    sys.exit(app.exec_())
