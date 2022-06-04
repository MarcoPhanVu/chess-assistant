# Cell.py

from Piece import Piece

from tkinter import Button
import tkinter.font as font
import copy
import time


class CellAI:
    def __init__(self):
        self.isOccupied         = False
        self.isTransformable    = False
        self.Score              = 0

        self.piece  = None
        self.loc    = None
        self.text   = None

    def showPossibleMoves(self, currentBoardState):

        """
        Parameters:
        - currentBoardState: Board object
        shows the current state of the chess board
        Return:
            - `listOfPossibleMoves`: list<list<2 integers>>
                tells all the possible moves of a piece ON this CELL
        Logic:
        `listOfLegalMoves` is a MUST-HAVE parameter 
        in the main area of the function, `listOfLegalMoves`
        will be used to check if it is any conflict like,
        move on the same cell or eat the same color piece.
        """
        if self.isOccupied == False:
            return list()

        listOfLegalMoves = list()
        name = self.piece.name


        if name == "king":
            listOfLegalMovesTEMP = [
                    [max(self.loc[0] - 1, 1), max(self.loc[1] - 1, 1)], # top    left  cell
                    [max(self.loc[0] - 1, 1),     self.loc[1]        ], # top          cell 
                    [max(self.loc[0] - 1, 1), min(self.loc[1] + 1, 8)], # top    right cell
                    [    self.loc[0]        , max(self.loc[1] - 1, 1)], #        left  cell
                    [    self.loc[0]        , min(self.loc[1] + 1, 8)], #        right cell
                    [min(self.loc[0] + 1, 8), max(self.loc[1] - 1, 1)], # bottom left  cell
                    [min(self.loc[0] + 1, 8),     self.loc[1]        ], # bottom       cell
                    [min(self.loc[0] + 1, 8), min(self.loc[1] + 1, 8)]  # bottom right cell
            ]

            for loc in listOfLegalMovesTEMP:
                if loc not in listOfLegalMoves:
                    listOfLegalMoves.append(loc)

            # check if the King is moved or not
            if self.piece.firstMoveTaken == False:
                row = self.loc[0]
                col = self.loc[1]
                leftCornerCell = currentBoardState.board[row-1][0]
                rightCornerCell = currentBoardState.board[row-1][7]

                checkAllLeftPath = [not currentBoardState.board[row-1][c].isOccupied for c in range(1, col-1)]
                checkAllRightPath = [not currentBoardState.board[row-1][c].isOccupied for c in range(col, 7)]
                if ((leftCornerCell.isOccupied) and
                    (leftCornerCell.piece.name == "rook") and
                    (leftCornerCell.piece.firstMoveTaken == False) and 
                    (all(checkAllLeftPath))):
                    listOfLegalMoves.append([row, col - 2])                 

                if ((rightCornerCell.isOccupied) and
                    (rightCornerCell.piece.name == "rook") and
                    (rightCornerCell.piece.firstMoveTaken == False) and
                    (all(checkAllRightPath))):
                    listOfLegalMoves.append([row, col + 2])


        elif name == "knight":
            delta = ["1","2"]
            operator = ["+", "-"]
            for i in range(len(delta)):
                i_ = (i+1)%2 # get the other delta number
                for j in range(len(operator)):
                    for k in range(len(operator)):
                        pairLoc = [
                            eval(f"{self.loc[0]} {operator[k]} {delta[i]}"),
                            eval(f"{self.loc[1]} {operator[j]} {delta[i_]}")]
                        if (1 <= pairLoc[0] <= 8) and (1 <= pairLoc[1] <= 8):
                            listOfLegalMoves.append(pairLoc)


        elif name == "pawn":
            pawn: Piece = self.piece
            orgRow = self.loc[0] - 1# index of current row
            orgCol = self.loc[1] - 1# index of current column
            
            # Pawn generally can only move one step a time
            # At starting position, pawn can take two steps forward.

            legalStep = 1 if pawn.firstMoveTaken else 2
    
            if pawn.isBlack:
                # I. MOVE
                # White pawn moves from row 2 (of index 1), towards row 8 (of index 7),
                # The row increases while the column stays the same
                # When the Cell ahead is occupied, pawn cannot travel.
                for step in range(1, legalStep + 1):
                    if currentBoardState.board[orgRow + step][orgCol].isOccupied:
                        break
                    listOfLegalMoves.append([orgRow + step + 1, orgCol + 1]) 

                # II. ATTACK
                # White pawn can attack diagonally,
                # if the diagonal Cell contains a Piece of opposite color   
                # handling right diagnal cell

                if orgCol < 7:
                    cellDiagnonalUpRight: Cell = currentBoardState.board[orgRow + 1][orgCol + 1]
                    if cellDiagnonalUpRight.isOccupied and pawn.isBlack != cellDiagnonalUpRight.piece.isBlack:
                        listOfLegalMoves.append(cellDiagnonalUpRight.loc)

                if orgCol > 0:
                    cellDiagnonalUpLeft: Cell = currentBoardState.board[orgRow + 1][orgCol - 1]
                    if cellDiagnonalUpLeft.isOccupied and pawn.isBlack != cellDiagnonalUpLeft.piece.isBlack:
                        listOfLegalMoves.append(cellDiagnonalUpLeft.loc)

                # EN PASSE
                if orgRow == 4:
                    if orgCol < 7:
                        cellAdjacentRight: Cell = currentBoardState.board[orgRow][orgCol + 1]
                        if cellAdjacentRight.isOccupied and cellAdjacentRight.piece.isEdibleEnPasse:
                            listOfLegalMoves.append([cellAdjacentRight.loc[0] + 1, cellAdjacentRight.loc[1]])

                    if orgCol > 0:
                        cellAdjacentLeft: Cell = currentBoardState.board[orgRow][orgCol - 1]
                        if cellAdjacentLeft.isOccupied and cellAdjacentLeft.piece.isEdibleEnPasse:
                            listOfLegalMoves.append([cellAdjacentLeft.loc[0] + 1, cellAdjacentLeft.loc[1]])

            else:
                # I. MOVE
                # Black pawn moves from row 8 (of index 7), towards row 1 (of index 0),
                # The row decreases while the column stays the same
                # When the Cell ahead is occupied, pawn cannot travel.
                for step in range(1, legalStep + 1):
                    if currentBoardState.board[orgRow - step][orgCol].isOccupied:
                        break
                    listOfLegalMoves.append([orgRow - step + 1, orgCol + 1]) 

                # II. ATTACK
                if orgCol < 7:
                    cellDiagnonalUpRight: Cell = currentBoardState.board[orgRow - 1][orgCol + 1]
                    if cellDiagnonalUpRight.isOccupied and pawn.isBlack != cellDiagnonalUpRight.piece.isBlack:
                        listOfLegalMoves.append(cellDiagnonalUpRight.loc)

                if orgCol > 0:
                    cellDiagnonalUpLeft: Cell = currentBoardState.board[orgRow - 1][orgCol - 1]
                    if cellDiagnonalUpLeft.isOccupied and pawn.isBlack != cellDiagnonalUpLeft.piece.isBlack:
                        listOfLegalMoves.append(cellDiagnonalUpLeft.loc)
                
                if orgRow == 3:
                    if orgCol < 7:
                        cellAdjacentRight: Cell = currentBoardState.board[orgRow][orgCol + 1]
                        if cellAdjacentRight.isOccupied and cellAdjacentRight.piece.isEdibleEnPasse:
                            listOfLegalMoves.append([cellAdjacentRight.loc[0] - 1, cellAdjacentRight.loc[1]])

                    if orgCol > 0:
                        cellAdjacentLeft: Cell = currentBoardState.board[orgRow][orgCol - 1]
                        if cellAdjacentLeft.isOccupied and cellAdjacentLeft.piece.isEdibleEnPasse:
                            listOfLegalMoves.append([cellAdjacentLeft.loc[0] - 1, cellAdjacentLeft.loc[1]])
            # WAITING "EN PASSE" situation


        else:
            #remove excess space + time defining the same functions
            orgRow = self.loc[0] - 1 #original Row Index
            orgCollumn = self.loc[1] - 1 #original Collumn Index


            def rookMoves(): #append Cells that are Legal for Rook (Tried to make a function but no use -> hardcode instead)
                #toUp
                for i in range(8 - orgRow - 1): #subtract 1 from the loop range to ensure everything is in the board

                    listOfLegalMoves.append(currentBoardState.board[orgRow + i + 1][orgCollumn].loc) #exclude it's own loc (loop start from 0 so we have to + 1)
                    if currentBoardState.board[orgRow + i + 1][orgCollumn].isOccupied: #End the loop when the last Cell is occupied(still take it's loc)
                        break
                
                # listOfLegalMoves.append([99, 99])

                #toDown
                for i in range(orgRow): #skip self.loc[0] by adding "-1"

                    listOfLegalMoves.append(currentBoardState.board[orgRow - i - 1][orgCollumn].loc)
                    if currentBoardState.board[orgRow - i - 1][orgCollumn].isOccupied:
                        break

                #toRight
                for i in range(8 - orgCollumn - 1):
                    listOfLegalMoves.append(currentBoardState.board[orgRow][orgCollumn + i + 1].loc)
                    if currentBoardState.board[orgRow][orgCollumn + i + 1].isOccupied:
                        break

                #toLeft
                for i in range(orgCollumn):
                    listOfLegalMoves.append(currentBoardState.board[orgRow][orgCollumn - i - 1].loc)
                    if currentBoardState.board[orgRow][orgCollumn - i - 1].isOccupied:
                        break

            
            def bishopMoves():
                tempRow = orgRow
                tempCol = orgCollumn

                # toUpperRight
                while tempRow < 8 and tempCol < 8:
                    tempCol += 1
                    tempRow += 1
                    if tempRow == 8 or tempCol == 8 or tempRow == -1 or tempCol == -1:
                        break
                    listOfLegalMoves.append(currentBoardState.board[tempRow][tempCol].loc)
                    if currentBoardState.board[tempRow][tempCol].isOccupied:
                        break

                #toUpperLeft
                tempRow = orgRow
                tempCol = orgCollumn
                while tempRow > -1 and tempCol < 8:
                    tempCol -= 1
                    tempRow += 1
                    if tempRow == 8 or tempCol == 8 or tempRow == -1 or tempCol == -1:
                        break
                    listOfLegalMoves.append(currentBoardState.board[tempRow][tempCol].loc)
                    if currentBoardState.board[tempRow][tempCol].isOccupied:
                        break

                #toLowerRight
                tempRow = orgRow

                tempCol = orgCollumn
                while tempRow < 8 and tempCol > -1:
                    tempCol += 1
                    tempRow -= 1
                    if tempRow == 8 or tempCol == 8 or tempRow == -1 or tempCol == -1:
                        break
                    listOfLegalMoves.append(currentBoardState.board[tempRow][tempCol].loc)
                    if currentBoardState.board[tempRow][tempCol].isOccupied:
                        break

                #toLowerLeft
                tempRow = orgRow
                tempCol = orgCollumn
                while tempRow > -1 and tempCol > -1:
                    tempCol -= 1
                    tempRow -= 1
                    if tempRow == 8 or tempCol == 8 or tempRow == -1 or tempCol == -1:
                        break
                    listOfLegalMoves.append(currentBoardState.board[tempRow][tempCol].loc)
                    if currentBoardState.board[tempRow][tempCol].isOccupied:
                        break


            if name == "rook":
                rookMoves()

            elif name == "bishop":
                bishopMoves()

            elif name == "queen":
                rookMoves()
                bishopMoves()

        listOfPossibleMoves = list()
        for cellLoc in listOfLegalMoves:
            if cellLoc == self.loc:
                continue


            possibleCell = currentBoardState.board[cellLoc[0] - 1][cellLoc[1] - 1]
            

            # listOfPossibleMoves.append(possibleCell)

            if not possibleCell.isOccupied:
                listOfPossibleMoves.append(possibleCell)
            elif possibleCell.piece.isBlack != self.piece.isBlack:
                listOfPossibleMoves.append(possibleCell)


        return listOfPossibleMoves

    def removePiece(self):
        self.isOccupied = False
        self.piece = None

    def setPiece(self, piece, firstMoveTaken=True):
        self.isOccupied = True
        self.piece = piece
        self.piece.firstMoveTaken = firstMoveTaken


class Cell(CellAI):
    YELLOW = "yellow"   # selected
    GREEN  = "green"    # possible move
    PURPLE = "purple"   # eat opponent
    RED    = "red"      # special move (castling, en passant, promotion)

    BLACK  = "darkgrey"
    WHITE  = "white"


    def __init__(self, boardState, loc, size, piece=None):

        self.isOccupied         = False
        self.isTransformable    = False
        self.Score              = 0

        self.boardState = boardState
        self.piece  = piece
        self.loc    = loc
        self.size   = size
        self.color  = self.getDefaultColor()
        self.text   = piece.getImage() if self.piece != None else ""

        self.button = Button(self.boardState.frm, text=self.text,
                             height=0, width=3,
                             command=self.click,
                             padx=size[0], pady=size[1]
                             ,compound="c")
        self.button["font"] = font.Font(size=36)
        self.button.config(bg=self.color)
        self.button.grid(column=loc[1], row=loc[0])
        self.button.bind("<Return>", self.invoke_button)

    def setColor(self, color):
        self.color = color
        self.button.configure(bg=self.color)

    def click(self):
        if self.boardState.isSelected == True and self.color not in (self.YELLOW, self.GREEN, self.PURPLE, self.RED):
            return
        if self.boardState.isSelected == False and self.isOccupied == False:
            return

        if self.color in (self.BLACK, self.WHITE):
            # if int(self.boardState.isBlackTurn) != self.piece.isBlack:
            #     return
            movableCells = self.showPossibleMoves(self.boardState)
            for cell in movableCells:
                cell.setColor(self.GREEN)
                # def isSpecialMove -> boolean
                # input:
                #   currCell -> var self: assert isOccupied
                #   moveableCell -> var cell:
                # Return:
                #   tell if moveableCell is special for pieces
            self.boardState.isSelected = True
            self.boardState.currentSelectedPiece = self.piece
            self.boardState.previousSelectedCell  = self
            self.setColor(self.YELLOW)
            self.removePiece()

        elif self.color == self.YELLOW:
            self.boardState.resetBoardColor()
            self.setPiece(self.boardState.currentSelectedPiece, self.boardState.currentSelectedPiece.firstMoveTaken)
            self.boardState.isSelected = False

        elif self.color == self.GREEN:

            self.boardState.resetBoardColor()
            self.boardState.resetEnPasse()
            self.setPiece(self.boardState.currentSelectedPiece)
            if (self.boardState.currentSelectedPiece.name == "pawn" and 
               (self.boardState.previousSelectedCell.loc[0] - self.loc[0]) in (-2, 2)
               ):
                self.boardState.currentSelectedPiece.isEdibleEnPasse = True
            
            self.boardState.isSelected = False
            # self.boardState.currentSelectedPiece = None
            self.boardState.previousSelectedCell.clear()
            self.boardState.isBlackTurn = not self.boardState.isBlackTurn
            self.boardState.saveState()

            # if self.boardState.isBlackTurn:
            #     nextMoveSuggestion = self.boardState.MakesRanDomMove(self.boardState)
            #     print(nextMoveSuggestion)
            #     self.boardState.moveGUI(nextMoveSuggestion[0], nextMoveSuggestion[1])
    def clear(self):
        self.resetColor()
        self.button['text'] = ""

    def setPiece(self, piece, firstMoveTaken=True):
        self.button["text"] = (piece.getImage())
        self.isOccupied = True
        self.piece = piece
        self.piece.firstMoveTaken = firstMoveTaken

    def getDefaultColor(self):
        return self.WHITE if ((self.loc[0] + self.loc[1]) % 2) else self.BLACK

    def removePiece(self):
        self.isOccupied = False
        self.piece = None

    def resetColor(self):
        self.color = self.getDefaultColor()
        self.button.configure(bg=self.color)

    def copy(self):
        """
        return: CellAI Object
        """
        cellAI = CellAI()
        cellAI.isOccupied         = self.isOccupied
        cellAI.isTransformable    = self.isTransformable
        cellAI.Score              = self.Score

        cellAI.piece  = copy.deepcopy(self.piece)
        cellAI.loc    = self.loc
        return cellAI



    def invoke_button(self, event):
        event.widget.config(relief = "sunken")
        self.root.update_idletasks()
        event.widget.invoke()
        time.sleep(0)
        event.widget.config(relief = "raised")
