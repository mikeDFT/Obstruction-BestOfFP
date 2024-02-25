
from unittest import TestCase
from domain.board import BoardClass
from domain.minimaxBoard import MiniMaxBoardClass
from domain import DomainError

class TestDomain(TestCase):
	def test_board(self):
		board = BoardClass()
		
		
		# making sure isMoveValid works fine in normal conditions
		self.assertEqual(board.isMoveValid(1, 1), True)
		self.assertEqual(board.isMoveValid(6, 6), True)
		self.assertEqual(board.isMoveValid(1, 7), False)
		self.assertEqual(board.isMoveValid(7, 1), False)
		self.assertEqual(board.isMoveValid("E", "WOW"), False)
		
		
		# it should raise a DomainError if raiseError is True and the move is invalid
		self.assertRaises(DomainError, board.isMoveValid, 10, 1, True)
		
		
		# making a move returns True if it works
		self.assertEqual(board.makeMove(True, 1, 1), True)
		
		
		# should not be valid as a move locks the 3x3 grid around the move location
		self.assertEqual(board.isMoveValid(1, 1), False)
		self.assertEqual(board.isMoveValid(1, 2), False)
		
		
		# making sure the board is not full
		self.assertEqual(board.gameOver, False)
		
		
		# making sure the moves list is not empty
		self.assertEqual(len(board.moves), 1)
		
		
		# available moves should be 32 (36 - 4)
		self.assertEqual(board.availableMoves(), 32)
		
		
		# if the move is not valid it should raise a DomainError
		self.assertRaises(DomainError, board.makeMove, True, 1, 1)
		
		
		# making sure these are the right instance types
		self.assertIsInstance(board.boardList, list)
		self.assertIsInstance(str(board), str)
	
	
	def test_minimaxBoard(self):
		board = MiniMaxBoardClass()
		
		
		# making sure isMoveValid works fine in normal conditions
		self.assertEqual(board.isMoveValid(1, 1), True)
		self.assertEqual(board.isMoveValid(6, 6), True)


		# making a move returns True if it works
		self.assertEqual(board.makeMove(1, 1), True)
		
		
		# should not be valid as a move locks the 3x3 grid around the move location
		self.assertEqual(board.isMoveValid(1, 1), False)
		
		
		# making sure the board is not full
		self.assertEqual(board.gameOver, False)
		
		
		# making sure the moves list is not empty
		self.assertEqual(len(board.moves), 1)
		
		
		# making sure these are the right instance types
		self.assertIsInstance(board.board, list)
		self.assertIsInstance(str(board), str)
		self.assertIsInstance(board.cloneBoard(), MiniMaxBoardClass)
		
		