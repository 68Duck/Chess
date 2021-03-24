from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from messageWindow import MessageWindow

class ChessWindow(QMainWindow,uic.loadUiType("chessWindow.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setupPieces()
        self.bKingMoved = False
        self.wKingMoved = False
        self.lbRookMoved = False
        self.rbRookMoved = False
        self.lwRookMoved = False
        self.rwRookMoved = False
        self.check = False
        self.gameOver = False

    def initUI(self):
        self.whiteTime = 300*100
        self.blackTime = 300*100
        self.whiteTimer.display(self.convertMilisecondsToMMSS(self.whiteTime))
        self.blackTimer.display(self.convertMilisecondsToMMSS(self.blackTime))
        self.whiteTurn = False
        self.changeTurn()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.decrimentTimer)
        self.timer.start(10)
        self.selectedSquare = None
        self.squares = []
        self.takeableSquares = []
        self.startX = 50
        self.startY = 50
        self.width = 75
        self.height = 75
        for i in range(8):
            for j in range(8):
                self.createSquare(self.startX,self.startY,self.width,self.height,i,j)

    def changeTurn(self):
        if self.whiteTurn:
            self.whiteTimer.setStyleSheet("background-color:#999;")
            self.blackTimer.setStyleSheet("background-color:black")
        else:
            self.blackTimer.setStyleSheet("background-color:#222")
            self.whiteTimer.setStyleSheet("background-color:white;")
        self.whiteTurn = not self.whiteTurn
        self.checkMessageLabel.setText("")

    def decrimentTimer(self):
        if self.whiteTurn:
            if self.whiteTime == 0 and not self.gameOver:
                self.messageWindow = MessageWindow("Black wins on time!")
                self.gameOver = True
            else:
                if not self.gameOver:
                    self.whiteTime -= 1
                    self.whiteTimer.display(self.convertMilisecondsToMMSS(self.whiteTime))
        else:
            if self.blackTime == 0 and not self.gameOver:
                self.gameOver = True
                self.messageWindow = MessageWindow("White wins on time!")
            else:
                if not self.gameOver:
                    self.blackTime -= 1
                    self.blackTimer.display(self.convertMilisecondsToMMSS(self.blackTime))

    def convertMilisecondsToMMSS(self,time):
        mins = time // 6000
        secs = time % 6000
        secs = secs//100
        if secs < 10:
            secs = "0" + str(secs)
        return str(mins)+":"+str(secs)


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
        self.newSquare.castling = False
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
        if pieceName == "disc":
            self.movePiece(squareNumber)
            self.deleteShownMoves()
            return

        elif square.pieceName != None:
            self.deleteShownMoves()
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
        if pieceName[len(pieceName)-1:len(pieceName)] == "W":
            colour = "white"
        else:
            colour = "black"
        promoted = False
        if squareNumber % 8 == 0 or squareNumber % 8 == 7:
            if pieceName[0:4] == "pawn":
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

        if self.squares[squareNumber].castling == True:
            if squareNumber == 15:
                self.squares[7].clear()
                self.squares[7].pieceName = None
                self.setSquarePiece(23,"rookW")
            elif squareNumber == 47:
                self.squares[63].clear()
                self.squares[63].pieceName = None
                self.setSquarePiece(39,"rookW")
            elif squareNumber == 8:
                self.squares[0].clear()
                self.squares[0].pieceName = None
                self.setSquarePiece(16,"rookB")
            elif squareNumber == 40:
                self.squares[56].clear()
                self.squares[56].pieceName = None
                self.setSquarePiece(32,"rookB")
        self.deleteShownMoves()
        if pieceName[0:4] == "king":
            if colour == "white":
                self.wKingMoved = True
            else:
                self.bKingMoved = True
        if pieceName[0:4] == "rook":
            for i in range(len(self.squares)):
                if self.selectedSquare == self.squares[i]:
                    initialLocation = i
            if colour == "white":
                if initialLocation == 7:
                    self.lwRookMoved = True
                else:
                    self.rwRookMoved = True
            else:
                if initialLocation == 0:
                    self.rbRookMoved = True #r is right as if facing as black
                else:
                    self.lbRookMoved = True
        self.changeTurn()

        checkMate = self.checkIfMate()
        if checkMate == True:
            self.messageWindow = MessageWindow("Checkmate!")
            self.gameOver = True

    def checkIfMate(self):
        for i in range(len(self.squares)):
            square = self.squares[i]
            pieceName = square.pieceName
            if pieceName is None:
                pass
            else:
                if pieceName[len(pieceName)-1:len(pieceName)] == "W":
                    colour = "white"
                else:
                    colour = "black"
                if (colour == "white" and self.whiteTurn) or (colour == "black" and not self.whiteTurn):
                    moves = self.getPossibleMoves(i,pieceName)
                    for move in moves:
                        try:
                            if len(move) > 1:
                                if move[1] == "pawn":
                                    if i >= 0 and i < 64:
                                        piece = self.checkIfPiece(i)
                                        if piece == False:
                                            pass
                                        else:
                                            if piece[len(piece)-1:len(piece)]=="W":
                                                if colour == "black":
                                                    return False
                                            else:
                                                if colour == "white":
                                                    return False
                        except:
                            piece = self.checkIfPiece(move)
                            if piece == False:

                                self.check = self.checkIfCheck(move,pieceName,i)
                                if not self.check:
                                    return False
                            else:
                                if piece[len(piece)-1:len(piece)]=="W":
                                    if pieceName[len(pieceName)-1:len(pieceName)] == "B":
                                        if pieceName[0:4] != "pawn":

                                            self.check = self.checkIfCheck(move,pieceName,i)
                                            # print(self.check,move,pieceName)
                                            if not self.check:
                                                return False
                                else:
                                    if pieceName[len(pieceName)-1:len(pieceName)] == "W":
                                        if pieceName[0:4] != "pawn":
                                            self.check = self.checkIfCheck(move,pieceName,i)
                                            if not self.check:
                                                return False
        return True



    def virtualGetPossibleMoves(self,squareNumber,pieceName,board):
        self.moves = []
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
                piece = self.virtualCheckIfPiece(squareNumber-1,board)
                if piece == False:
                    valid = True
                else:
                    valid = False
                self.moves.append(squareNumber-1)
                if squareNumber%8==6 and valid:
                    self.moves.append(squareNumber-2)
                    # print("can move twice")
                self.moves.append([squareNumber-9,"pawn"])
                self.moves.append([squareNumber+7,"pawn"])

            else: #so black pawn
                if squareNumber * 8 == 7:
                    self.promotePawn(squareNumber,colour)
                    return
                piece = self.virtualCheckIfPiece(squareNumber+1,board)
                if piece == False:
                    valid = True
                else:
                    valid = False
                self.moves.append(squareNumber+1)
                if squareNumber%8==1 and valid:
                    self.moves.append(squareNumber+2)
                self.moves.append([squareNumber+9,"pawn"])
                self.moves.append([squareNumber-7,"pawn"])
        if pieceName[0:6] == "knight":

            if not left:
                if not top:
                    if not twoTop:
                        self.moves.append(squareNumber-10)
                    if not twoLeft:
                        self.moves.append(squareNumber-17)
                if not bottom:
                    if not twoBottom:
                        self.moves.append(squareNumber-6)
                    if not twoLeft:
                        self.moves.append(squareNumber-15)
            if not right:
                if not top:
                    if not twoTop:
                        self.moves.append(squareNumber+6)
                    if not twoRight:
                        self.moves.append(squareNumber+15)
                if not bottom:
                    if not twoBottom:
                        self.moves.append(squareNumber+10)
                    if not twoRight:
                        self.moves.append(squareNumber+17)
        if pieceName[0:4] == "king":
            if colour == "white":
                if not self.check:
                    if self.wKingMoved == False:
                        if self.lwRookMoved == False:
                            if not self.virtualCheckIfPiece(15,board) and not self.virtualCheckIfPiece(23,board):
                                self.moves.append([15,"castling"])
                        if self.rwRookMoved == False:
                            if not self.virtualCheckIfPiece(39,board) and not self.virtualCheckIfPiece(47,board) and not self.virtualCheckIfPiece(55,board):
                                self.moves.append([47,"castling"])
            else:
                if self.bKingMoved == False:
                    if self.lbRookMoved == False:
                        if not self.virtualCheckIfPiece(48,board) and not self.virtualCheckIfPiece(40,board) and not self.virtualCheckIfPiece(32,board):
                            self.moves.append([40,"castling"])
                    if self.rbRookMoved == False:
                        if not self.virtualCheckIfPiece(8,board) and not self.virtualCheckIfPiece(16,board):
                            self.moves.append([8,"castling"])

            if not left:
                self.moves.append(squareNumber-8)
                if not top:
                    self.moves.append(squareNumber-9)
                if not bottom:
                    self.moves.append(squareNumber-7)
            if not right:
                self.moves.append(squareNumber+8)
                if not top:
                    self.moves.append(squareNumber+7)
                if not bottom:
                    self.moves.append(squareNumber+9)
            if not top:
                self.moves.append(squareNumber-1)
            if not bottom:
                self.moves.append(squareNumber+1)



        if pieceName[0:4] == "rook":
            row = squareNumber % 8 #will return 0-7
            for i in range(row):
                self.moves.append(squareNumber-i-1)
                valid = self.virtualCheckIfPiece(squareNumber-i-1,board)
                if valid:
                    break
            for i in range(7-row):
                self.moves.append(squareNumber+i+1)
                valid = self.virtualCheckIfPiece(squareNumber+i+1,board)
                if valid:
                    break
            column = squareNumber//8
            for i in range(column):
                self.moves.append(squareNumber-8*(i+1))
                valid = self.virtualCheckIfPiece(squareNumber-8*(i+1),board)
                if valid:
                    break
            for i in range(7-column):
                self.moves.append(squareNumber+8*(i+1))
                valid = self.virtualCheckIfPiece(squareNumber+8*(i+1),board)
                if valid:
                    break
        if pieceName[0:6] == "bishop":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break

        if pieceName[0:5] == "queen":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.virtualCheckIfPiece(displaySquare,board)
                    if piece:
                        break
            row = squareNumber % 8 #will return 0-7
            for i in range(row):
                self.moves.append(squareNumber-i-1)
                valid = self.virtualCheckIfPiece(squareNumber-i-1,board)
                if valid:
                    break
            for i in range(7-row):
                self.moves.append(squareNumber+i+1)
                valid = self.virtualCheckIfPiece(squareNumber+i+1,board)
                if valid:
                    break
            column = squareNumber//8
            for i in range(column):
                self.moves.append(squareNumber-8*(i+1))
                valid = self.virtualCheckIfPiece(squareNumber-8*(i+1),board)
                if valid:
                    break
            for i in range(7-column):
                self.moves.append(squareNumber+8*(i+1))
                valid = self.virtualCheckIfPiece(squareNumber+8*(i+1),board)
                if valid:
                    break
        return self.moves


    def getPossibleMoves(self,squareNumber,pieceName):
        self.moves = []
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
                piece = self.checkIfPiece(squareNumber-1)
                if piece == False:
                    valid = True
                else:
                    valid = False
                self.moves.append(squareNumber-1)
                if squareNumber%8==6 and valid:
                    self.moves.append(squareNumber-2)
                    # print("can move twice")
                self.moves.append([squareNumber-9,"pawn"])
                self.moves.append([squareNumber+7,"pawn"])

            else: #so black pawn
                if squareNumber * 8 == 7:
                    self.promotePawn(squareNumber,colour)
                    return
                piece = self.checkIfPiece(squareNumber+1)
                if piece == False:
                    valid = True
                else:
                    valid = False
                self.moves.append(squareNumber+1)
                if squareNumber%8==1 and valid:
                    self.moves.append(squareNumber+2)
                self.moves.append([squareNumber+9,"pawn"])
                self.moves.append([squareNumber-7,"pawn"])
        if pieceName[0:6] == "knight":

            if not left:
                if not top:
                    if not twoTop:
                        self.moves.append(squareNumber-10)
                    if not twoLeft:
                        self.moves.append(squareNumber-17)
                if not bottom:
                    if not twoBottom:
                        self.moves.append(squareNumber-6)
                    if not twoLeft:
                        self.moves.append(squareNumber-15)
            if not right:
                if not top:
                    if not twoTop:
                        self.moves.append(squareNumber+6)
                    if not twoRight:
                        self.moves.append(squareNumber+15)
                if not bottom:
                    if not twoBottom:
                        self.moves.append(squareNumber+10)
                    if not twoRight:
                        self.moves.append(squareNumber+17)
        if pieceName[0:4] == "king":
            if colour == "white":
                if not self.check:
                    if self.wKingMoved == False:
                        if self.lwRookMoved == False:
                            if not self.checkIfPiece(15) and not self.checkIfPiece(23):
                                self.moves.append([15,"castling"])
                        if self.rwRookMoved == False:
                            if not self.checkIfPiece(39) and not self.checkIfPiece(47) and not self.checkIfPiece(55):
                                self.moves.append([47,"castling"])
            else:
                if self.bKingMoved == False:
                    if self.lbRookMoved == False:
                        if not self.checkIfPiece(48) and not self.checkIfPiece(40) and not self.checkIfPiece(32):
                            self.moves.append([40,"castling"])
                    if self.rbRookMoved == False:
                        if not self.checkIfPiece(8) and not self.checkIfPiece(16):
                            self.moves.append([8,"castling"])

            if not left:
                self.moves.append(squareNumber-8)
                if not top:
                    self.moves.append(squareNumber-9)
                if not bottom:
                    self.moves.append(squareNumber-7)
            if not right:
                self.moves.append(squareNumber+8)
                if not top:
                    self.moves.append(squareNumber+7)
                if not bottom:
                    self.moves.append(squareNumber+9)
            if not top:
                self.moves.append(squareNumber-1)
            if not bottom:
                self.moves.append(squareNumber+1)



        if pieceName[0:4] == "rook":
            row = squareNumber % 8 #will return 0-7
            for i in range(row):
                self.moves.append(squareNumber-i-1)
                valid = self.checkIfPiece(squareNumber-i-1)
                if valid:
                    break
            for i in range(7-row):
                self.moves.append(squareNumber+i+1)
                valid = self.checkIfPiece(squareNumber+i+1)
                if valid:
                    break
            column = squareNumber//8
            for i in range(column):
                self.moves.append(squareNumber-8*(i+1))
                valid = self.checkIfPiece(squareNumber-8*(i+1))
                if valid:
                    break
            for i in range(7-column):
                self.moves.append(squareNumber+8*(i+1))
                valid = self.checkIfPiece(squareNumber+8*(i+1))
                if valid:
                    break
        if pieceName[0:6] == "bishop":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break

        if pieceName[0:5] == "queen":
            row = squareNumber % 8
            column = squareNumber // 8
            for i in range(7):
                displaySquare = squareNumber-7*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 0:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber-9*(i+1)
                if displaySquare < 0 or displaySquare % 8 == 7:
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+7*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 7:#7 as checks if moved around to the bottom
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            for i in range(7):
                displaySquare = squareNumber+9*(i+1)
                if displaySquare > 63 or displaySquare % 8 == 0: #0 as checks if moved around to the top
                    break
                else:
                    self.moves.append(displaySquare)
                    piece = self.checkIfPiece(displaySquare)
                    if piece:
                        break
            row = squareNumber % 8 #will return 0-7
            for i in range(row):
                self.moves.append(squareNumber-i-1)
                valid = self.checkIfPiece(squareNumber-i-1)
                if valid:
                    break
            for i in range(7-row):
                self.moves.append(squareNumber+i+1)
                valid = self.checkIfPiece(squareNumber+i+1)
                if valid:
                    break
            column = squareNumber//8
            for i in range(column):
                self.moves.append(squareNumber-8*(i+1))
                valid = self.checkIfPiece(squareNumber-8*(i+1))
                if valid:
                    break
            for i in range(7-column):
                self.moves.append(squareNumber+8*(i+1))
                valid = self.checkIfPiece(squareNumber+8*(i+1))
                if valid:
                    break
        return self.moves

    def showMoves(self,square,pieceName,squareNumber):
        moves = self.getPossibleMoves(squareNumber,pieceName)
        for move in moves:
            try:
                if len(move) > 1:
                    if move[1] == "castling":
                        self.displayMoveOption(move[0],pieceName,castling=True)
                    elif move[1] == "pawn":
                        self.displayIfTakeable(move[0],pieceName)
            except:
                self.displayMoveOption(move,pieceName)


    def displayIfTakeable(self,squareNumber,currentPiece):
        if squareNumber >= 0 and squareNumber < 64:
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


    def displayMoveOption(self,squareNumber,currentPiece,castling=False):
        piece = self.checkIfPiece(squareNumber)
        if piece == False:
            self.check = self.checkIfCheck(squareNumber,currentPiece)
            if self.check:
                return False
            self.setSquarePiece(squareNumber,"disc")
            self.squares[squareNumber].pieceName="disc"
            if castling:
                self.squares[squareNumber].castling = True
            return True
        else:
            # print(piece[len(piece)-1:len(piece)])
            if piece[len(piece)-1:len(piece)]=="W":
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "B":
                    if currentPiece[0:4] != "pawn":
                        self.check = self.checkIfCheck(squareNumber,currentPiece)
                        if self.check:
                            return False
                        self.addTakeableView(squareNumber)
                    return False #returns false meaning cannot move beyond here
                else:
                    return False
            else:
                # print(currentPiece[len(currentPiece)-1:len(currentPiece)])
                if currentPiece[len(currentPiece)-1:len(currentPiece)] == "W":
                    # self.addRing(squareNumber)
                    if currentPiece[0:4] != "pawn":
                        self.check = self.checkIfCheck(squareNumber,currentPiece)
                        if self.check:
                            return False
                        self.addTakeableView(squareNumber)
                    return False #returns false meaning cannot move beyond here
                else:
                    return False


    def checkIfPiece(self,squareNumber):
        if self.squares[squareNumber].pieceName is None:
            return False
        else:
            return self.squares[squareNumber].pieceName

    def virtualCheckIfPiece(self,squareNumber,board):
        if board[squareNumber] is None:
            return False
        else:
            return board[squareNumber]

    def checkIfCheck(self,squareNumber,currentPiece,selectedSquareNumber = None):
        currentBoard = []
        for square in self.squares:
            if square.pieceName == "disc":
                currentBoard.append(None)
            else:
                currentBoard.append(square.pieceName)
        if selectedSquareNumber is None:
            for i in range(len(self.squares)):
                if self.squares[i] == self.selectedSquare:
                    selectedSqr = i
        else:
            selectedSqr = selectedSquareNumber
        currentBoard[selectedSqr] = None
        currentBoard[squareNumber] = currentPiece
        totalMoves = []
        # print(currentBoard)

        for i in range(len(currentBoard)):
            # square = self.squares[i]
            pieceName = currentBoard[i]
            if pieceName != None:
                if pieceName[len(pieceName)-1:len(pieceName)] == "W":
                    pieceColour = "white"
                elif pieceName[len(pieceName)-1:len(pieceName)] == "B":
                    pieceColour = "black"
                else:
                    pass #therefore a disc
                if self.whiteTurn:
                    if pieceColour == "black":
                        moves = self.virtualGetPossibleMoves(i,pieceName,currentBoard)
                        movesToRemove = []
                        for move in moves:
                            try:
                                if len(move)>1:
                                    movesToRemove.append(move)
                                    if move[0] >= 0 and move[0] < 64:
                                        moves.append(move[0])
                            except:
                                piece = self.virtualCheckIfPiece(move,currentBoard)
                                if piece is False:
                                    virtualPieceColour = None
                                else:
                                    virtualPieceColour = piece[len(piece)-1:len(piece)]
                                if piece != False and virtualPieceColour == "B":
                                    movesToRemove.append(move)
                        for move in movesToRemove:
                            moves.remove(move)
                        for move in moves:
                            totalMoves.append(move)
                else:
                    if pieceColour == "white":
                        moves = self.virtualGetPossibleMoves(i,pieceName,currentBoard)
                        movesToRemove = []
                        for move in moves:
                            try:
                                if len(move)>1:
                                    movesToRemove.append(move)
                                    if move[0] < 64 and move[0] >=0:
                                        moves.append(move[0])
                            except:
                                piece = self.virtualCheckIfPiece(move,currentBoard)
                                if piece is False:
                                    virtualPieceColour = None
                                else:
                                    virtualPieceColour = piece[len(piece)-1:len(piece)]

                                if piece != False and virtualPieceColour == "W":
                                    movesToRemove.append(move)
                        for move in movesToRemove:
                            moves.remove(move)
                        for move in moves:
                            totalMoves.append(move)
        if self.whiteTurn:
            for i in range(len(currentBoard)):
                pieceName = currentBoard[i]
                if pieceName == "kingW":
                    kingSquare = i
            if kingSquare in totalMoves:
                self.checkMessageLabel.setText("Check!")
                # print("check")
                return True
        else:
            for i in range(len(currentBoard)):
                pieceName = currentBoard[i]
                if pieceName == "kingB":
                    kingSquare = i
            if kingSquare in totalMoves:
                self.checkMessageLabel.setText("Check!")
                # print("check")
                return True
        return False

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
                self.squares[i].castling = False

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
