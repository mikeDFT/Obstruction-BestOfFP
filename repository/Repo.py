
from domain.board import BoardClass

"""
This repository is made just for the sake of abiding by the layered architecture rules
It only holds 1 domain object, the board
"""


class RepositoryClass:
	def __init__(self):
		self.__board = BoardClass()
	
	
	@property
	def board(self):
		return self.__board
	
	
	
	