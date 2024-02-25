from domain import DomainError
from services import ServicesError, MainService
from ui import UIError

class ConsoleClass:
	def __init__(self):
		self.running = True  # should be accessible from outside
		self.__gameOver = False
	
	
	def __handleMainMenu(self):
		self.__printMainMenu()
		userInput = self.__getInput()
		
		if userInput in ("s1", "s2", "start1", "start2"):
			self.__services = MainService.MainServiceClass()
			
			# the first move by AI is random, what's the fun in having the AI always play the same move in the beginning?
			if userInput in ("s2", "start2"):
				self.__services.AIFirstMove()
			
			self.__gameOver = False
			while not self.__gameOver:
				# catching most Exceptions here
				try:
					self.__handleGameMenu()
				except ValueError as ve:
					print("[ValueError]:" + str(ve))
				except (DomainError, ServicesError, UIError) as err:
					print(err)
		elif userInput == "exit":
			self.running = False
			return
		else:
			raise UIError("Invalid input")
	
	
	def __handleGameMenu(self):
		# checking if the game is over to end it before input
		print(self.__services.boardStr)
		
		if self.__services.isGameOver():
			self.__printGameOutcome(False) # human lost
			self.__gameOver = True
			return
		
		self.__printGameMenu()
		userInput = self.__getInput()
		
		if userInput == "back":
			self.__gameOver = True
			return
		else:
			didHumanWin = self.__services.makeHumanMove(userInput)
			
			if didHumanWin:
				print(self.__services.boardStr)
				self.__printGameOutcome(True) # human won
				self.__gameOver = True
				return
			
			# TODO send choice to services
			
	
	def start(self):
		while self.running:
			# __handleMainMenu can only raise UIError for invalid input, all the other Exceptions get caught in there
			try:
				self.__handleMainMenu()
			except UIError as err:
				print(err)
	
	
	@staticmethod
	def __getInput():
		return input("[Choose an instruction]: ").lower()
	
	
	@staticmethod
	def __printGameMenu():
		print("/-----------------------------------------------------------\\")
		print("|--------------------- <[ GAME MENU ]> ---------------------|")
		print("|-   <row> <column>                                        -|")
		print("|-   back                                                  -|")
		print("\\-----------------------------------------------------------/")
	
	
	@staticmethod
	def __printMainMenu():
		print("/-----------------------------------------------------------\\")
		print("|--------------------- <[ MAIN MENU ]> ---------------------|")
		print("|-   start1 / s1       (you make first move)               -|")
		print("|-   start2 / s2       (AI makes first move)               -|")
		print("|-   exit                                                  -|")
		print("\\-----------------------------------------------------------/")
	
	
	@staticmethod
	def __printGameOutcome(humanWon: bool):
		print("/-----------------------------------------------------------\\")
		print("|---------------------- <[ OUTCOME ]> -----------------------|")
		
		if humanWon:
			print("|-                         YOU WON                          -|")
		else:
			print("|-                         YOU LOST                         -|")
			
		print("\\-----------------------------------------------------------/")
		
		