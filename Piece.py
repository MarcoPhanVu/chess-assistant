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
		# 	- name: string
		# 		accepted: [king, queen, pawn, rook, bishop, knight]
		# 	- isBlack: bool
		# 		accepted: []
		# Attributes:
		# 	- name: 		string
		#   - isBlack: 		bool
		# 	- image: 		string, accept one of special char
		# 	- isAlive:		bool
		# 	- SCORE:		integer, used for Minimax algo
		# Method:
		# 	- move()
		
		self.name = name
		self.isBlack = int(isBlack) # 1 if Black, 0 if White

		# Raise KeyError if `name` not in `imageDatabase`
		self.image = Piece.imageDatabase[self.name][self.isBlack] # ♔ ♚ ♕ ♛ ♗ ♝ ♘ ♞ ♙ ♟ ♖ ♜
		self.isAlive = True
  
	def setImage(self):
		return self.image
	
	def printImage(self):
		print(self.image)
		# print(self.image.encode("utf-8"))
  
rookWhite = Piece("rook", True)
rookBlack = Piece("rook", False)

# print(rookWhite)
# print(f"name of rW = {rookWhite.name}")

rookWhite.printImage()
rookBlack.printImage()