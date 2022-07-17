# Board.py
from Piece import *
from Cell import Cell
from tkinter import *
from tkinter import ttk
import copy
import random
from datetime import datetime

class BoardAI:
    historyBoards = list()

    #Lists(to prevent re-declaration over and over again to preserve memory)

    def __init__(self):
        self.board = list()
        self.isBlackTurn = None

    def updateHistory(self):
        self.historyBoards.append(self)

    def printBoardWPieceTerminal(self) -> None:

        BOARD_SIDE = range(8)
        print('   ' + '   '.join([str(col_num) for col_num in BOARD_SIDE]) )
        row_num = 0
        for row in self.board:
            print(' ' + ' ---' * 8) 
            print(str(row_num) + '', end='')
            for cell in row:
                if cell.isOccupied == False:
                    print('|   ', end='')
                else:
                    print(f'| {cell.piece.getImage()} ', end='')
            print('|')
            row_num += 1
        print('  ' + ' ---' * 8) 
        print()

    def moveAI(self, oldLoc, newLoc, optionPromotion=None):
        oldCell = self.board[oldLoc[0]][oldLoc[1]]
        newCell = self.board[newLoc[0]][newLoc[1]]

        newCell.type = oldCell.isSpecialMove(newCell)
        newCell.setPiece(oldCell.piece)
        oldCell.removePiece()

        if newCell.type > 0:
            if newCell.type == 3:
                newCell.doSpecialMove(self, optionPromotion, True)
            else:
                newCell.doSpecialMove(self)


    def getScore(self):
        # return random.uniform(-1,1)
        totalScoreWhite = 0
        totalScoreBlack = 0

        pawnMultiplier = [1, 1, 1, 1.5, 2, 2.5, 3]

        for row in self.board:
            for cell in row:
                if not cell.isOccupied:
                    continue
                piece = cell.piece
                if piece.isBlack:
                    if piece.name == "pawn":

                        # totalScoreBlack += cell.piece.SCORE
                        totalScoreBlack += piece.SCORE * pawnMultiplier[cell.loc[0] - 2] #Black -> increasing index
                        # [might need this] print(f"This {cell.piece.name} is currently at {cell.loc[0]}-{cell.loc[1]} and have a score of {cell.piece.SCORE * pawnMultiplier[cell.loc[0] - 2]}")
                    else:
                        totalScoreBlack += piece.SCORE
                else:
                    if piece.name == "pawn":
                        # totalScoreWhite += cell.piece.SCORE
                        totalScoreWhite += piece.SCORE * pawnMultiplier[7 - cell.loc[0]] #White -> decreasing index
                    else:
                        totalScoreWhite += piece.SCORE

        return (totalScoreBlack - totalScoreWhite)

    def copy(self):
        """
        return: BoardAI Object
        """
        boardAI = BoardAI()
        boardAI.isBlackTurn = self.isBlackTurn
        for row in self.board:
            newRow = list()
            for cell in row:
                newRow.append(cell.copy())
            boardAI.board.append(newRow)

        return boardAI

    def alphaBetaPrunning(self, succ, a, b, isMax):
        if isMax:
            newAlpha = max(a if succ[2] == None else succ[2], a)
            return newAlpha
        else:
            newBeta = min(b if succ[2] == None else succ[2], b)
            return newBeta


    def minimax(self, successor, depth=4, isMaximizePlayer=True, alpha=-100000, beta=100000):
        """
        successor contains four objects:
            - Current State of the board: BoardAI
            - Next move: [oldLoc, newLoc], None in the first depth
            - The Score for the next move: Float number,
            - Option for promotion: 0=Knight, 3=Queen, None=NotPromotion/FirstDepth
        """
        # random.seed((datetime.now().timestamp())*100000)
        if depth == 0 or alpha >= beta:
            # print(successor)
            return successor
        boardState = successor[0]
        historicalMoves = [] if successor[1] == None else successor[1]
        listOfInputForMoves = []
        
        if isMaximizePlayer:
            for i, row in enumerate(boardState.board):
                for j, cell in enumerate(row):
                    if (cell.isOccupied) and \
                       (cell.piece.isBlack == isMaximizePlayer):
                        oldLoc = [i, j] #-> all Loc -1
                        listOfMoveableCell = cell.showPossibleMoves(boardState)
                        for newCell in listOfMoveableCell:
                            newLoc = [newCell.loc[0] - 1 , newCell.loc[1] - 1]
                            listOfInputForMoves.append([oldLoc, newLoc])
            

            successor = list()
            # print(len(listOfInputForMoves))
            for eachSuggestion in listOfInputForMoves:
                oldLoc = eachSuggestion[0]
                newLoc = eachSuggestion[1]
                # check if the is promotion move
                if boardState.board[oldLoc[0]][oldLoc[1]]\
                    .isSpecialMove(boardState.board[newLoc[0]][newLoc[1]]) == 3:
                    # version for Knight
                    copiedVersionKnight = copy.deepcopy(boardState)
                    copiedVersionKnight.moveAI(oldLoc, newLoc, 0)
                    successorKnight = self.minimax(
                        [copiedVersionKnight, historicalMoves + [eachSuggestion], copiedVersionKnight.getScore(), 0],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)
                    # version for Queen
                    copiedVersionQueen = copy.deepcopy(boardState)
                    copiedVersionQueen.moveAI(oldLoc, newLoc, 3)
                    successorQueen = self.minimax(
                        [copiedVersionQueen, historicalMoves + [eachSuggestion], copiedVersionQueen.getScore(), 3],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)
                    
                    if successorQueen[2] > successorKnight[2]:
                        newSuccessor = successorQueen
                    else:
                        newSuccessor = successorKnight

                else:

                    # copiedVersion = copy.deepcopy(boardState)
                    copiedVersion = boardState.copy()
                    copiedVersion.moveAI(oldLoc, newLoc)
                    newSuccessor = self.minimax(
                        [copiedVersion, historicalMoves + [eachSuggestion], copiedVersion.getScore(), None],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)

                successor.append(newSuccessor)
                alpha = self.alphaBetaPrunning(newSuccessor, alpha, beta, isMaximizePlayer)
                # if isBreak:
                #     break

            successor.sort(key = lambda x: x[2], reverse = isMaximizePlayer)
            optimalScore = successor[0][2]
            listOfEqualMoves = [s for s in successor if s[2] == optimalScore]

        else:
            for i, row in enumerate(boardState.board):
                for j, cell in enumerate(row):
                    if (cell.isOccupied) and \
                       (cell.piece.isBlack == isMaximizePlayer):
                        oldLoc = [i, j] #-> all Loc -1
                        listOfMoveableCell = cell.showPossibleMoves(boardState)
                        for newCell in listOfMoveableCell:
                            newLoc = [newCell.loc[0] - 1 , newCell.loc[1] - 1]
                            listOfInputForMoves.append([oldLoc, newLoc])
            successor = list()
            for eachSuggestion in listOfInputForMoves:
                oldLoc = eachSuggestion[0]
                newLoc = eachSuggestion[1]
                # check if the is promotion move

                if boardState.board[oldLoc[0]][oldLoc[1]]\
                    .isSpecialMove(boardState.board[newLoc[0]][newLoc[1]]) == 3:
                    # version for Knight
                    copiedVersionKnight = copy.deepcopy(boardState)
                    copiedVersionKnight.moveAI(oldLoc, newLoc, 0)

                    successorKnight = self.minimax(
                        [copiedVersionKnight, historicalMoves + [eachSuggestion], copiedVersionKnight.getScore(), 0],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)
                    
                    # version for Queen
                    copiedVersionQueen = copy.deepcopy(boardState)
                    copiedVersionQueen.moveAI(oldLoc, newLoc, 3)
                    successorQueen = self.minimax(
                        [copiedVersionQueen, historicalMoves + [eachSuggestion], copiedVersionQueen.getScore(), 3],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)
                    
                    if successorQueen[2] < successorKnight[2]:
                        newSuccessor = successorQueen
                    else:
                        newSuccessor = successorKnight

                else:

                    # copiedVersion = copy.deepcopy(boardState)
                    copiedVersion = boardState.copy()
                    copiedVersion.moveAI(oldLoc, newLoc)
                    newSuccessor = self.minimax(
                        [copiedVersion, historicalMoves + [eachSuggestion], copiedVersion.getScore(), None],
                        depth-1, not isMaximizePlayer,
                        alpha, beta)

                successor.append(newSuccessor)
                beta = self.alphaBetaPrunning(newSuccessor, alpha, beta, isMaximizePlayer)

            successor.sort(key = lambda x: x[2], reverse = isMaximizePlayer)
            optimalScore = successor[0][2]
            listOfEqualMoves = [s for s in successor if s[2] == optimalScore]

        finalOption = random.choice(listOfEqualMoves)
        return finalOption

    def MakesRanDomMove(self, currState):
        initSuccessor = [currState.copy(), None, None, None]
        # adjust the depth of the minimax function below to advance the
        # the calculator.
        # Note: the deeper the algo goes, the longer it took to find the optimal moves
        s = self.minimax(initSuccessor,3)
        s[0].printBoardWPieceTerminal()
        return s[1][0], s[2], s[3]


class Board(BoardAI):

    mainPanel = Tk()

    def __init__(self):
        self.frm = ttk.Frame(self.mainPanel)
        self.frm.grid()
        self.board = list()
        self.isSelected = False
        self.previousSelectedCell  = None
        self.currentSelectedPiece = None
        self.isBlackTurn = False
        
        for x in range(8):
            row = list()
            for y in range(8):
                cell = Cell(self, [x + 1, y + 1], [0, 0])
                row.append(cell)

            self.board.append(row)

        pieceList = ["rook", "knight", "bishop", "pawn", "queen", "king"]
        #Kings always stays on the E Collumn
        for i in range(2):
            self.board[0][3 + i].setPiece(Piece(pieceList[4 + i], True), False)
            self.board[7][3 + i].setPiece(Piece(pieceList[4 + i], False), False)

        for i in range(3):
            self.board[0][i].setPiece(Piece(pieceList[i], True), False)
            self.board[0][7-i].setPiece(Piece(pieceList[i], True), False)
            self.board[7][i].setPiece(Piece(pieceList[i], False), False)
            self.board[7][7-i].setPiece(Piece(pieceList[i], False), False)

        for i in range(8):
            self.board[1][i].setPiece(Piece(pieceList[3], True), False)
            self.board[6][7-i].setPiece(Piece(pieceList[3], False), False) 


    def resetBoardColor(self):
        boardCell = self.board
        for row in  boardCell:
            for cell in row:
                cell.resetColor()

    def resetEnPasse(self):
        boardCell = self.board
        for row in  boardCell:
            for cell in row:
                if cell.isOccupied:
                    cell.piece.isEdibleEnPasse = False

    def getBoard(self):
        return self.board

    def visualize(self):
        self.mainPanel.mainloop()
        pass

    def moveGUI(self, oldLoc, newLoc, optionPromotion=None):

        oldCell = self.board[oldLoc[0]][oldLoc[1]]
        newCell = self.board[newLoc[0]][newLoc[1]]
        
        oldCell.click()
        newCell.click(optionPromotion)

    def saveState(self):

        newBoardState = self.copy()
        newBoardState.updateHistory()

    def freeze(self):
        for row in self.board:
            for cell in row:
                cell.button['state'] = "disabled"

    def release(self):
        for row in self.board:
            for cell in row:
                cell.button['state'] = "normal"

    