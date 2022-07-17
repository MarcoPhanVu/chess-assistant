# Piece.py
class Piece:
    
    imageDatabase = {
        'king': ('♔', '♚'),
        'queen': ('♕', '♛'),
        'rook': ('♖', '♜'),
        'knight': ('♘', '♞'),
        'bishop': ('♗', '♝'),
        'pawn': ('♙', '♟')
    }
    
    def __init__(self, name, isBlack):
        # Parameters
        #   - name: string
        #       accepted: [king, queen, pawn, rook, bishop, knight]
        #   - isBlack: bool
        #       accepted: []
        # Attributes:
        #   - name:         string
        #   - isBlack:      bool
        #   - image:        string, accept one of special char
        #   - isAlive:      bool
        #   - SCORE:        integer, used for Minimax algo
        # Method:
        #   - move()
        
        self.name = name
        self.isBlack = int(isBlack) # 1 if Black, 0 if White

        # Raise KeyError if `name` not in `imageDatabase`
        self.image = Piece.imageDatabase[self.name][self.isBlack] # ♔ ♚ ♕ ♛ ♗ ♝ ♘ ♞ ♙ ♟ ♖ ♜
        self.isAlive = True
        self.firstMoveTaken = False
        self.isEdibleEnPasse = False
        
        self.SCORE = None
        if self.name == "king": self.SCORE = 10000000
        if self.name == "queen": self.SCORE = 1000
        if self.name == "rook": self.SCORE = 600
        if self.name == "bishop": self.SCORE = 450
        if self.name == "knight": self.SCORE = 300
        if self.name == "pawn": self.SCORE = 30

        
    def getName(self):
        return self.name

    def getImage(self):
        return self.image
    
    def printImage(self):
        print(self.image)
