
import pickle
from random import randint
from repository.Repo import RepositoryClass
from domain.minimaxBoard import MiniMaxBoardClass

class AIClass:
	def __init__(self, repo: RepositoryClass):
		self.__repo = repo
		self.__bestMove = None
		
		# the first move of the AI is always gonna be one of the 4, no reason to not store them and wait like 10 sec
		# for the AI to keep computing it
		self.__bestFirstMoves = [(1, 1), (1, 6), (6, 6), (6, 1)]
		self.__minAvailableMovesForCache = 20
		
		# opening the cache file
		try:
			cacheFile = open("files/AICache.bin", "rb")
			self.__cache = pickle.load(cacheFile)
		except (FileNotFoundError, EOFError):
			self.__cache = {}
			# it's inside looks like this:
			"""
			{
				20 = [  # 20 is the available moves from that position and the moves before are the moves done by others
					{ "moves": board.moves, "bestMove": move },
					{ "moves": board.moves, "bestMove": move },
					{ "moves": board.moves, "bestMove": move },
					...
				],
				21 = [
					...
				]
			}
			"""
	
	
	def getRndMove(self):  # no longer used
		"""
		:return: random row and col values that are valid
		"""
		row = randint(1, 6)
		col = randint(1, 6)
		
		while not self.__repo.board.isMoveValid(row, col):
			row = randint(1, 6)
			col = randint(1, 6)
		
		return row, col
	
	
	def makeFirstMove(self):
		"""
		the first move of the AI is always gonna be in a corner
		makes a move at the coordinates of one of the corners
		"""
		rndBestMove = self.__bestFirstMoves[randint(0, len(self.__bestFirstMoves)-1)]
		self.__repo.board.makeMove(False, *rndBestMove)


	def makeMove(self):
		"""
		makes an AI move
		"""
		availableMoves = self.__repo.board.availableMoves()
		if availableMoves >= self.__minAvailableMovesForCache:
			move = self.__getMoveFromCache(availableMoves)
			if move:
				self.__repo.board.makeMove(False, *move)
				return
			
		self.__repo.board.makeMove(False, *self.__getBestMove())
	
	
	def __getMoveFromCache(self, availableMoves: int) -> list | None:
		"""
		gets the best possible move from cache
		:param availableMoves: number of available moves
		:return: the move or None if there isn't one cached already
		"""
		moves = self.__getSortedMoves() # current board moves sorted
		
		if availableMoves in self.__cache:
			for moveDict in self.__cache[availableMoves]:
				if moveDict["moves"] == moves:  # they've both been ordered so this works as it should
					return moveDict["bestMove"]
	
	
	def saveCache(self):
		"""
		saves the cache file
		"""
		
		try:
			cacheFile = open("files/AICache.bin", "wb")
			pickle.dump(self.__cache, cacheFile)
		except FileNotFoundError:
			pass
	
	
	@staticmethod
	def __sortKey(move): # key function used for sorting moves
		return move[0], move[1]
	
	
	def __getSortedMoves(self) -> list:
		"""
		sorts the moves list
		:return: the sorted list of the moves
		"""
		
		moves = self.__repo.board.moves
		moves.sort(key=self.__sortKey)
		
		return moves
	
	
	def __addMoveToCache(self, availableMoves: int):
		"""
		adds a move to cache
		:param availableMoves: number of available moves
		"""
		
		if availableMoves not in self.__cache:
			self.__cache[availableMoves] = []
		
		moves = self.__getSortedMoves()
		
		self.__cache[availableMoves].append({
			"moves": moves,
			"bestMove": self.__bestMove
		})
	
	
	def __getBestMove(self):
		"""
		uses the minimax algorithm to get the best possible move
		:return: the best possible move
		"""
		
		minimaxBoard = MiniMaxBoardClass(self.__repo.board.boardList)
		
		_maxScore = self.__minimax(minimaxBoard, 0, -1000, 1000, True)
		
		availableMoves = self.__repo.board.availableMoves()
		if availableMoves >= self.__minAvailableMovesForCache:
			self.__addMoveToCache(availableMoves)
		
		return self.__bestMove[0], self.__bestMove[1]
	
	
	def __minimax(self, board: MiniMaxBoardClass, depth: int, alpha: int, beta: int, maximizingPlr: bool) -> int:
		"""
		Uses the minimax AI algorithm to determine the best move that the AI can make
		also uses alpha-beta pruning to optimize it
		sources: https://www.neverstopbuilding.com/blog/minimax, https://youtu.be/l-hh51ncgDI?si=Wzdoo5bBo2j9j4sG&t=533
		:param board: minimax board made for the minimax algorithm to optimize it
		:param depth: used to make sure the AI is fighting more when losing and ends it quicker when winning
		:param alpha, beta: values used to prune options to save computational time
		(view this for a visual representation: https://youtu.be/l-hh51ncgDI?si=Wzdoo5bBo2j9j4sG&t=533)
		:param maximizingPlr: if True, it's our turn, and we want the game to end after it. winning +10, losing -10
		:return: the score of that position (assuming both players play optimally), also puts the best move in self.__bestMove as a list
		"""
		
		if board.gameOver:
			# if the game is already over, and it's AI's turn: -10 (lose), if it's the human's turn: 10 (win)
			# depth-10 if losing so that the AI fights to play more rounds
			# 10-depth if winning so that the AI ends it sooner
			return maximizingPlr and depth-10 or 10-depth
		
		availableMoves = []
		
		# getting all the empty squares where we can move
		for row in range(1, 7):
			for col in range(1, 7):
				if board.isMoveValid(row, col):
					availableMoves.append([row, col])
		
		if maximizingPlr:
			# maximizingPlayer = True  if it's AI's turn and is trying to max the score
			maxScore = -100
			bestMove = None
			
			for move in availableMoves:
				newBoard = board.cloneBoard()
				newBoard.makeMove(*move)
				
				score = self.__minimax(newBoard, depth + 1, alpha, beta, not maximizingPlr)
				
				if score > maxScore:
					maxScore = score
					bestMove = move
				
				# pruning
				alpha = max(maxScore, alpha)
				if alpha >= beta:
					break
			
			self.__bestMove = bestMove
			return maxScore
		else:
			# maximizingPlayer = False  if it's human's turn and is trying to min the score for AI
			minScore = 100
			bestMove = None
			
			for move in availableMoves:
				newBoard = board.cloneBoard()
				newBoard.makeMove(*move)
				
				score = self.__minimax(newBoard, depth + 1, alpha, beta, not maximizingPlr)
				
				if score < minScore:
					minScore = score
					bestMove = move
				
				# pruning
				beta = min(minScore, beta)
				if alpha >= beta:
					break
			
			self.__bestMove = bestMove
			return minScore
	
	