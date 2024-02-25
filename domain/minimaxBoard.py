
"""
Made to optimize the minimax algorithm as it's pretty heavy
"""
from texttable import Texttable


class MiniMaxBoardClass:
	def __init__(self, clonedBoard: list = None, clonedMoves: list = None):
		self.__board = []
		self.moves = clonedMoves or []
		
		# can also be created as a clone of another board
		if not clonedBoard:
			for i in range(6):
				self.__board.append([])
				for j in range(6):
					self.__board[-1].append("")
		else:
			self.__board = clonedBoard
	
	def isMoveValid(self, row: int, col: int) -> bool:
		"""
		Checks if a move is valid (doesn't have too many redundant checks, to make it faster)
		:param row: row on board
		:param col: column on board
		:return: True if the move is valid, False otherwise
		"""
		
		if self.__board[row-1][col-1] != "":
			return False
		
		return True
	
	def makeMove(self, row: int, col: int) -> bool:
		"""
		Makes a move on the board
		:param row: row on board
		:param col: column on board
		:return: True if the move was made
		"""
		
		self.moves.append({
			"row": row,
			"col": col
		})
		
		row -= 1
		col -= 1
		
		# fills squares around the move with locked blocks
		for i in range(row - 1, row + 2):
			for j in range(col - 1, col + 2):
				if 0 <= i <= 5 and 0 <= j <= 5 and self.__board[i][j] == "":
					self.__board[i][j] = "M"
		
		return True
	
	def cloneBoard(self):
		"""
		:return: a clone of the board to use in minimax branches and not modify the original board
		"""
		return MiniMaxBoardClass(self.board, self.moves.copy())
	
	@property
	def gameOver(self) -> bool:
		"""
		checking if board is full
		:return: True if the board is full, False otherwise
		"""
		
		for i in range(0, 6):
			for j in range(0, 6):
				if self.__board[i][j] == "":
					return False
		
		return True
	
	@property
	def board(self):
		"""
		:return: a copy of the board, so as to not be modified from outside
		"""
		newBoard = []
		
		for i in range(6):
			newBoard.append(self.__board[i].copy())
		
		return newBoard  # returns a copy of the board so that it can't be modified from outside
	
	def __str__(self) -> str:
		"""
		:return: a string representation of the board
		"""
		
		txtTable = Texttable()
		
		txtTable.add_row([" "] + [i for i in range(1, 7)])
		for i in range(0, 6):
			txtTable.add_row([i + 1] + self.__board[i])
		
		return txtTable.draw()
	
	