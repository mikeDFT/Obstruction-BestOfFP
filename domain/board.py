
from texttable import Texttable
from domain import DomainError

class Characters: # somewhat like an Enum dictionary
	EMPTY = ""
	AI = "X"
	HUMAN = "O"
	LOCKED = "#" # Full block
	
	# set at runtime
	allChars = []
	L = None # Locked
	E = None # Empty
	
	def __init__(self):
		Characters.allChars = [Characters.EMPTY, Characters.AI, Characters.HUMAN, Characters.LOCKED]
		Characters.L = Characters.LOCKED
		Characters.E = Characters.EMPTY


class BoardClass:
	def __init__(self):
		"""
		"" - empty
		"X" - Computer
		"O" - O
		"L" - Locked
		"""
		Characters() # init characters
		self.__board = []
		self.__moves = []
		
		# init board
		for i in range(6):
			self.__board.append([])
			for j in range(6):
				self.__board[-1].append("")
	
	def isMoveValid(self, row: int, col: int, raiseError: bool = False):
		"""
		verify if a move is valid or not
		:param row: row on board
		:param col: column on board
		:param raiseError: if True, raises DomainError if the move is invalid
		:return: True if the move is valid, False otherwise (if raiseError is False, if raiseError is True it raises DomainError)
		"""
		
		if not isinstance(row, int) or not isinstance(col, int):
			if raiseError:
				raise DomainError("[BoardError]: row and column must be integers")
			else:
				return False
		
		if not (1 <= row <= 6 and 1 <= col <= 6):
			if raiseError:
				raise DomainError("[BoardError]: row and column must be between 1 and 6")
			else:
				return False
		
		row -= 1
		col -= 1
		
		if self.__board[row][col] != Characters.EMPTY:
			if raiseError:
				raise DomainError("[BoardError]: move is not valid")
			else:
				return False
		
		return True
	
	@property
	def moves(self):
		"""
		:return: a copy of the moves list, so as to not be modified from outside
		"""
		
		moves = []
		for m in self.__moves:
			moves.append(m.copy())
		
		return moves
	
	@property
	def gameOver(self) -> bool:
		"""
		Checks if the board is full
		:return: True if the board is full, False otherwise
		"""
		for i in range(0, 6):
			for j in range(0, 6):
				if self.__board[i][j] == Characters.EMPTY:
					return False
		
		return True
	
	def makeMove(self, isHuman: bool, row: int, col: int):
		"""
		Makes a move on the board
		:param isHuman: True if the move is made by the human, False if by the AI
		:param row: row on board
		:param col: column on board
		:return: True if the move was made, None otherwise
		"""
		
		# raises DomainError if the move is invalid
		self.isMoveValid(row, col, True)
		
		row -= 1
		col -= 1
		
		# fills squares around the move with locked blocks
		for i in range(row - 1, row + 2):
			for j in range(col - 1, col + 2):
				if 0 <= i <= 5 and 0 <= j <= 5:
					self.__board[i][j] = Characters.LOCKED
		
		self.__moves.append([row, col])
		
		# adding the move
		if isHuman:
			self.__board[row][col] = Characters.HUMAN
		else:
			self.__board[row][col] = Characters.AI
		
		return True
	
	@property
	def boardList(self):
		"""
		:return: a copy of the board list, so as to not be modified from outside
		"""
		newBoard = []
		
		for i in range(6):
			newBoard.append(self.__board[i].copy())
			
		return newBoard  # returns a copy of the board so that it can't be modified from outside
	
	def availableMoves(self) -> int:
		"""
		:return: the number of available moves
		"""
		
		nr = 0
		
		for row in range(6):
			for col in range(6):
				if self.__board[row][col] == Characters.EMPTY:
					nr += 1
		
		return nr
	
	def __str__(self) -> str:
		"""
		:return: the board as a string
		"""
		
		txtTable = Texttable()
		
		txtTable.add_row([" "] + [i for i in range(1, 7)])
		for i in range(0, 6):
			txtTable.add_row([i+1] + self.__board[i])
		
		return txtTable.draw()

	
	
	
	