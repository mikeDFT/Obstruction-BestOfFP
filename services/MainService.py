
from services import AIService, ServicesError
from repository.Repo import RepositoryClass

class MainServiceClass:
	def __init__(self):
		self.__repo = RepositoryClass()
		self.__AI = AIService.AIClass(self.__repo)
	
	
	def AIFirstMove(self):
		"""
		calls the makeFirstMove function from the AIService
		"""
		self.__AI.makeFirstMove()
	
	
	def makeAIMove(self):
		"""
		calls the makeMove function from the AIService
		"""
		self.__AI.makeMove()
	
	
	def makeHumanMove(self, userInput: str) -> bool:
		"""
		Validates user input and sends it to the HumanService
		:param: userInput: str - user input
		:return: bool - True if the human won, False otherwise
		"""
		
		# validating user input
		choice = userInput.split(" ")
		if len(choice) != 2 or not self.__is_int(choice[0]) or not self.__is_int(choice[1]):
			raise ServicesError("Invalid move")
		
		row, col = int(choice[0]), int(choice[1])
		
		# sending the move to the HumanService
		self.__repo.board.makeMove(True, row, col)
		
		# checking if the game is over to end it before AI move
		if self.isGameOver():
			return True
		
		# if the game is not over, the AI makes a move right after the human move
		self.makeAIMove()
		
	
	def isGameOver(self) -> bool:
		"""
		Saves cache if the game is over
		:return: bool - True if the game is over, False otherwise
		"""
		
		gameOver = self.__repo.board.gameOver
		
		if gameOver: # saving cache at the end of the game
			self.__AI.saveCache()
		
		return gameOver
	
	
	@property
	def boardStr(self) -> str:
		"""
		:return: the board as a string (for printing)
		"""
		
		return str(self.__repo.board)
	
	
	@staticmethod
	def __is_int(nr):
		"""
		:return: int(nr) or False if it doesn't exist (without raising ValueError)
		"""
		
		try:
			return int(nr)
		except ValueError:
			return False
	
	
	def getBoardState(self):
		"""
		:return: the board state (for GUI, to update the score)
		"""
		
		return self.__repo.board.boardList
	
	