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
        self.selectedSquare = None
        self.whiteTurn = True
        self.squares = []
        self.takeableSquares = []
        self.startX = 50
        self.startY = 50
        self.width = 75
        self.height = 75
        for i in range(8):
            for j in range(8):
                self.createSquare(self.startX,self.startY,self.width,self.height,i,j)

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

    def addTakeableView(self,squareNumber):
        self.squares[squareNumber].setStyleSheet("background-color:yellow;")
        self.takeableSquares.append(self.squares[squareNumber])

    # def addRing(self,squareNumber):
    #     # self.setSquarePiece(squareNumber,"ring")
    #     # square = self.squares[squareNumber]
    #     # size = square.size()
    #     # self.newRing = QLabel(self,alignment=Qt.AlignCenter)
    #     # self.newRing.setFixedSize(size.width(),size.height())
    #     # self.newRing.move(square.x(),square.y())
    #     # # self.newRing.move(20,20)
    #     # pixmap = QPixmap("ring.png")
    #     # self.newRing.setPixmap(pixmap.scaled(75,75,Qt.KeepAspectRatio))
    #     # self.newRing.setStyleSheet("background-color:white;")
    #     # print(size.width(),size.height())
    #     # print(square.x(),square.y())

    def setSquarePiece(self,squareNumber,pieceName): #square number is 0 indexed. Piece 0 is top left and moved down first
        if pieceName != False:
            pixmap = QPixmap(f"{pieceName}.png")
            self.squares[squareNumber].setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))
            self.squares[squareNumber].pieceName = pieceName
        else:
            self.squares[squareNumber].clear()#removes the pixmap
            self.squares[squareNumber].pieceName = None

    def createSquare(self,startX,startY,width,height,x,y):
        self.newSquare = QLabel(self,alignment=Qt.AlignCenter)
        self.newSquare.setFixedSize(width,height)
        self.newSquare.move(startX+width*x,startY+height*y)
        self.newSquare.pieceName = None
        self.newSquare.selected = False
        # self.newSquare.clicked.connect(self.squareClicked)
        if (x+y)%2==1:
            self.newSquare.setStyleSheet("background-color:#769656; border: 1px solid black;")
            self.newSquare.colour = "black"
        else:
            self.newSquare.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
            self.newSquare.colour = "white"
        self.squares.append(self.newSquare)

    def squareClicked(self,squareNumber):
        square = self.squares[squareNumber]
        pieceName = square.pieceName
        if pieceName is None:
            pass
        else:
            if pieceName[len(pieceName)-1:len(pieceName)] == "W":
                pieceColour = "white"
            else:
                pieceColour = "black"
        if self.squares[squareNumber] in self.takeableSquares:
            self.movePiece(squareNumber)
            return
        self.deleteShownMoves()
        if pieceName == "disc":
            self.movePiece(squareNumber)
            return

        elif square.pieceName != None:
            self.updateSelection(square)
            if self.whiteTurn:
                if pieceColour == "white":
                    self.showMoves(square,pieceName,squareNumber)
            else:
                if pieceColour == "black":
                    self.showMoves(square,pieceName,squareNumber)


        if pieceName is None:
            return#finish me

    def movePiece(self,squareNumber):
        pieceName = self.selectedSquare.pieceName
        promoted = False
        if squareNumber % 8 == 0 or squareNumber % 8 == 7:
            if pieceName[0:4] == "pawn":
                print("test")
                if pieceName[4:5] == "W":
                    colour = "white"
                else:
                    colour = "black"
                self.promotePawn(squareNumber,colour)
                promoted = True
        self.selectedSquare.clear()
        self.selectedSquare.pieceName = None
        if self.selectedSquare.colour == "white":
            self.selectedSquare.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
        else:
            self.selectedSquare.setStyleSheet("background-color:#769656; border: 1px solid black;")
        if not promoted:
            self.setSquarePiece(squareNumber,pieceName)
        self.deleteShownMoves()
        self.whiteTurn = not self.whiteTurn


    def showMoves(self,square,pieceName,squareNumber):
        falses = []
        for i in range(8):
            falses.append(False)
        left,right,top,bottom,twoLeft,twoRight,twoTop,twoBottom = falses
        if squareNumber >= 8 and squareNumber < 16:
            twoLeft = True
        if squareNumber < 56 and squareNumber >= 48:
            twoRight = True
        if squareNumber % 8 == 1:
            twoTop = True
        if squareNumber % 8 == 6:
            twoBottom = True
        if squareNumber < 8:
            left = True
        if squareNumber >= 56:
            right = True
        if squareNumber % 8 == 0:
            top = True
        if squareNumber % 8 == 7:
            bottom = True
        if pieceName[len(pieceName)-1:len(pieceName)] == "B": #black piece
            colour = "black"
        else: #white piece
            colour = "white"
        if pieceName[0:4] == "pawn":
            if colour == "white":
                valid = self.displayMoveOption(squareNumber-1,pieceName)
                if squareNumber%8==6 and valid:
                    self.displayMoveOption(squareNumber-2,pieceName)
                    # print("can move twice")
                self.displayIfTakeable(squareNumber-9,pieceName)
                self.displayIfTakeable(squareNumber+7,pieceName)

            else: #so black pawn
                if squareNumber * 8 == 7:
                    self.promotePawn(squareNumber,colour)
                    return
                valid = self.displayMoveOption(squareNumber+1,pieceName)
                if squareNumber%8==1 and valid:
                    self.displayMoveOption(squareNumber+2,pieceName)
                    # print("can move twice")
                self.displayIfTakeable(squareNumber+9,pieceName)
                self.displayIfTakeable(squareNumber-7,pieceName)
        if pieceName[0:6] == "knight":

            if not left:
                if not top:
                    if not twoTop:
                        self.displayMoveOption(squareNumber-10,pieceName)
                    if not twoLeft:
                        self.displayMoveOption(squareNumber-17,pieceName)
                if not bottom:
                    if not twoBottom:
                        self.displayMoveOption(squareNumber-6,pieceName)
                    if not twoLeft:
                        self.displayMoveOption(squareNumber-15,pieceName)
            if not right:
                if not top:
                    if not twoTop:
                        self.displayMoveOption(squareNumber+6,pieceName)
                    if not twoRight:
                        self.displayMoveOption(squareNumber+15,pieceName)
                if not bottom:
                    if not twoBottom:
                        self.displayMoveOption(squareNumber+10,pieceName)
                    if not twoRight:
                        self.displayMoveOption(squareNumber+17,pieceName)
        if pieceName[0:4] == "king":
            if not left:
                self.displayMoveOption(squareNumber-8,pieceName)
                if not top:
                    self.displayMoveOption(squareNumber-9,pieceName)
                if not bottom:
                    self.displayMoveOption(squareNumber-7,pieceName)
            if not right:
                self.displayMoveOption(squareNumber+8,pieceName)
                if not top:
                    self.displayMoveOption(squareNumber+7,pieceName)
                if not bottom:
                    self.displayMoveOption(squareNumber+9,pieceName)
            if not top:
                self.displayMoveOption(squareNumber-1,pieceName)
            if not bottom:
                self.displayMoveOption(squareNumber+1,pieceName)
        if pieceName[0:4] == "rook":
            row = squareNumber % 8 #will return 0-7
            for i in range(row):
                valid = self.displayMoveOption(squareNumber-i-1,pieceName)
                if not valid:
                    break
            for i in range(7-row):
                valid = self.displayMoveOption(squareNumber+i+1,pieceName)
                if not valid:
                    break
            column = squareNumber//8
            for i in range(column):
                print(squareNumber-8*(i))
                valid = self.displayMoveOption(squareNumber-8*(i+1),pieceName)
                if not valid:
                    break
            for i in range(7-column):
                valid = self.displayMoveOption(squareNumber+8*(i+1),pieceName)
                if not valid:
                    break
        if pieceName[0:6] == "bishop":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break

        if pieceName[0:5] == "queen":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    valid = self.displayMoveOption(displaySquare,pieceName)
                    if not valid:
                        break
            for i in range(row):
                valid = self.displayMoveOption(squareNumber-i-1,pieceName)
                if not valid:
                    break
            for i in range(7-row):
                valid = self.displayMoveOption(squareNumber+i+1,pieceName)
                if not valid:
                    break
            for i in range(column):
                print(squareNumber-8*(i))
                valid = self.displayMoveOption(squareNumber-8*(i+1),pieceName)
                if not valid:
                    break
            for i in range(7-column):
                valid = self.displayMoveOption(squareNumber+8*(i+1),pieceName)
                if not valid:
                    break


    def displayIfTakeable(self,squareNumber,currentPiece):
        piece = self.checkIfPiece(squareNumber)
        if piece == False:
            return False
        else:
            if piece[len(piece)-1:len(piece)]=="W":
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "B":
                    self.addTakeableView(squareNumber)
                    return True
                else:
                    return False
            else:
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "W":
                    self.addTakeableView(squareNumber)
                    return True
                else:
                    return False


    def displayMoveOption(self,squareNumber,currentPiece):
        piece = self.checkIfPiece(squareNumber)
        if piece == False:
            self.setSquarePiece(squareNumber,"disc")
            self.squares[squareNumber].pieceName="disc"
            return True
        else:
            # print(piece[len(piece)-1:len(piece)])
            if piece[len(piece)-1:len(piece)]=="W":
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "B":
                    if currentPiece[0:4] != "pawn":
                        self.addTakeableView(squareNumber)
                    return False #returns false meaning cannot move beyond here
                else:
                    return False
            else:
                # print(currentPiece[len(currentPiece)-1:len(currentPiece)])
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "W":
                    # self.addRing(squareNumber)
                    if currentPiece[0:4] != "pawn":
                        self.addTakeableView(squareNumber)
                    return False #returns false meaning cannot move beyond here
                else:
                    return False


    def checkIfPiece(self,squareNumber):
        if self.squares[squareNumber].pieceName is None:
            return False
        else:
            return self.squares[squareNumber].pieceName

    def promotePawn(self,squareNumber,colour):
        #add choose ability so not just queen
        if colour == "white":
            self.setSquarePiece(squareNumber,"queenW")
        else:
            self.setSquarePiece(squareNumber,"queenB")





    def updateSelection(self,newSelectedSquare):
        if newSelectedSquare.selected == False:
            if self.selectedSquare:
                self.selectedSquare.selected = False
                if self.selectedSquare.colour == "white":
                    self.selectedSquare.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
                else:
                    self.selectedSquare.setStyleSheet("background-color:#769656; border: 1px solid black;")
            newSelectedSquare.selected = True
            newSelectedSquare.setStyleSheet("background-color:#BACA2B;")
            self.selectedSquare = newSelectedSquare
        for square in self.takeableSquares:
            if square.colour == "white":
                square.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
            else:
                square.setStyleSheet("background-color:#769656; border: 1px solid black;")

    def deleteShownMoves(self):
        for i in range(len(self.squares)):
            if self.squares[i].pieceName == "disc":
                self.setSquarePiece(i,False)
                self.squares[i].pieceName=None

        for square in self.takeableSquares:
            if square.colour == "white":
                square.setStyleSheet("background-color:#eeeed2; border: 1px solid black;")
            else:
                square.setStyleSheet("background-color:#769656; border: 1px solid black;")
        self.takeableSquares = []

    def mousePressEvent(self,e):
        x = e.x()
        y = e.y()
        if x > self.startX and x < self.startX+8*self.width:
            if y > self.startY and y < self.startY+8*self.height:
                xRange = (x-self.startX)/self.width
                yRange = (y-self.startY)/self.height
                for i in range(8):
                    if i > xRange:
                        i-=1
                        xPos = i
                        break
                for j in range(8):
                    if j > yRange:
                        j-=1
                        ypos = j
                        break
                squareNumber = i*8+j
                self.squareClicked(squareNumber)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = ChessWindow()
    win.show()
    sys.exit(app.exec_())
