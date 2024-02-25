
import pygame

from unittest import TestCase
from services.MainService import MainServiceClass
from services.AIService import AIClass
from services.SoundsManager import SoundError, SoundManagerClass
from services import ServicesError
from repository.Repo import RepositoryClass
from domain.board import BoardClass


"""
This test takes a long time because AI doesn't have certain moves in the cache so it has to be computed every time
"""

class TestServices(TestCase):
	def test_main_service(self):
		mainService = MainServiceClass()
		
		# making a move returns True if the human won
		self.assertNotEqual(mainService.makeHumanMove("2 2"), True)
		
		
		# making sure the game is not over yet
		self.assertNotEqual(mainService.isGameOver(), True)
		
		
		# making sure it returns the appropriate instance types
		self.assertIsInstance(mainService.getBoardState(), list)
		
		self.assertIsInstance(mainService.boardStr, str)
		
		self.assertIsInstance(mainService.getBoardState(), list)
		
		self.assertIsInstance(mainService.isGameOver(), bool)
		
		"""
		I can't test much more as the rest is up to the AI (which I'm also trying to test below)
		"""
	
	
	def test_ai_service(self):
		repo = RepositoryClass()
		AI = AIClass(repo)
		
		"""
		This test takes a long time because AI doesn't have certain moves in the cache so it has to be computed every time
		"""
		
		# testing return value types
		self.assertIsInstance(AI.getRndMove(), tuple)
		row, col = AI.getRndMove()
		
		self.assertIsInstance(row, int)
		self.assertIsInstance(col, int)
		
		
		# checking the number of moves on the board
		self.assertEqual(len(repo.board.moves), 0)
		
		AI.makeFirstMove()
		
		
		# checking the number of moves on the board
		self.assertEqual(len(repo.board.moves), 1)
		
		AI.makeMove()
		
		
		# checking the number of moves on the board
		self.assertEqual(len(repo.board.moves), 2)
		
		AI.makeMove()
		
		
		# checking the number of moves on the board
		self.assertEqual(len(repo.board.moves), 3)
		
		
		# making sure the game is not over yet
		self.assertNotEqual(repo.board.gameOver, True)
		
		
	def test_sounds_manager(self):
		pygame.init() # needs to be initialized before using the SoundManagerClass
		soundsManager = SoundManagerClass("../sounds/")
		
		# should raise a SoundError if the sound is not found or invalid
		self.assertRaises(SoundError, soundsManager.playSound, "notfound")
		
		self.assertRaises(SoundError, soundsManager.playSound, False)
		
		self.assertRaises(SoundError, soundsManager.playSound, 123)
		
		self.assertIsInstance(str(soundsManager), str)
