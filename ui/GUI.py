
import pygame

from domain import DomainError
from services import ServicesError, MainService
from ui import UIError
from services.SoundsManager import SoundManagerClass, SoundError
from ui.ColorEnums import ColorEnums
from ui.GUIObject import GUIObjectClass

"""
"All modules with the exception of the UI will have specifications and PyUnit test cases"
As it's part of the UI, it doesn't require comments, but I added them so that it's easier to understand what's going on
"""

class GUIClass:
	def __init__(self):
		# from docs: "It is safe to call this init() more than once as repeated calls will have no effect.
		# This is true even if you have pygame.quit() all the modules."
		pygame.init()
		# window title
		pygame.display.set_caption('Obstruction - Ban Mihai 911')
		# window icon
		Icon = pygame.image.load("images/icon.png")
		pygame.display.set_icon(Icon)
		
		self.__ColorEnums = ColorEnums()
		self.__service = MainService.MainServiceClass()
		self.__soundManager = SoundManagerClass()
		
		# vars
		self.__state = "Main Menu"
		self.__gameState = ""  # "won" / "lost" to show the labels
		self.__running = True
		self.__score = [0, 0]
		
		# fonts
		self.__titlefont = pygame.font.SysFont("Impact", 150)
		self.__creditsfont = pygame.font.SysFont("Impact", 35)
		self.__textfont = pygame.font.SysFont("Corbel", 35)
		self.__tilefont = pygame.font.SysFont("ComicSans", 80)
		self.__outcomefont = pygame.font.SysFont("Impact", 60)
		
		# screen stuff
		self.__screen_size = {
			"width": 800,
			"height": 600
		}
		self.__screen = pygame.display.set_mode((self.__screen_size["width"], self.__screen_size["height"]))
		
		# dictionary of active events (all events that have been binded and haven't been unbinded)
		self.__Events = [{
			"ID": -10, # unbindable event
			"Type": pygame.QUIT,
			"Func": self.__quitGame,
		}]
		
		# objects are added here after the user hovers over said object and the sound is played but the mouse
		# hasn't left the object yet, this is to not play the sound too many times
		self.__hoveredDebounce = []
		
		self.__MainMenuButtons = []
		self.__initMainMenu()
		
		self.__GameButtons = []
		self.__initGame()
	
	
	# GAME
	def __isTileBinded(self, buttonDict):
		ID = buttonDict["row"] * 10 + buttonDict["col"]
		for i in range(len(self.__Events)):
			if self.__Events[i]["ID"] == ID:
				return True
		return False
	
	
	def __resetGameGUI(self):
		for buttonDict in self.__GameButtons:
			buttonDict["Object"].buttonColor = ColorEnums.TILE_ORANGE
			buttonDict["Object"].beText(self.__tilefont, "")
			
			# if the player hit Quit, there are remaining tiles that haven't been unbinded
			# we need to bind the remaining unbinded (from locked) tiles again
			if not self.__isTileBinded(buttonDict):
				ID = buttonDict["row"] * 10 + buttonDict["col"]
				
				self.__bindButton(buttonDict["Object"], "Game", ID, self.__makeMove, [buttonDict["row"], buttonDict["col"]], extraArgsHover={
					"init": ColorEnums.TILE_ORANGE,
					"hover": ColorEnums.TILE_LIGHT_ORANGE
				})
	
	
	def __getButtonDictFromRowCol(self, row, col):
		for buttonDict in self.__GameButtons:
			if buttonDict["row"] == row and buttonDict["col"] == col:
				return buttonDict
	
	
	def __updateTile(self, row, col, state):
		# updates a tile at row=row, col=col, state=state
		
		buttonDict = self.__getButtonDictFromRowCol(row, col)
		
		if state == "#":
			buttonDict["Object"].buttonColor = ColorEnums.TILE_LOCKED
			buttonDict["Object"].beText(self.__tilefont, "")
			
			self.__unbind(row*10 + col)
		elif state == "O":
			buttonDict["Object"].buttonColor = ColorEnums.TILE_LOCKED
			buttonDict["Object"].beText(self.__tilefont, "O", ColorEnums.BLUE)
			
			self.__unbind(row * 10 + col)
		elif state == "X":
			buttonDict["Object"].buttonColor = ColorEnums.TILE_LOCKED
			buttonDict["Object"].beText(self.__tilefont, "X", ColorEnums.RED)
			
			self.__unbind(row * 10 + col)
	
	def __updateAllTiles(self):
		# updating all the tiles
		
		boardState = self.__service.getBoardState()
		
		for i in range(6):
			for j in range(6):
				self.__updateTile(i + 1, j + 1, boardState[i][j])
	
	def __initGame(self):
		# initializing game GUI
		
		# adding a padding so that add the exit button from the game
		padding = 30
		shiftDown = 50
		shiftRight = 45
		spaceBetween = 7
		width = self.__screen_size["width"] - padding*2
		height = self.__screen_size["height"] - padding*2
		
		startX = (width - height) // 2
		rateX = (width - startX * 2) // 6 - 5
		startX += shiftRight

		startY = padding
		rateY = (height - startY * 2) // 6
		startY += shiftDown
		
		# this is just so that it works with different widths and heights, but I prefer symmetry over it
		# if width > height:
		# 	startX = (width - height) // 2
		# 	rateX = (width - startX * 2) // 6
		# 	startX += shift
		#
		# 	startY = padding
		# 	rateY = (height - startY * 2) // 6
		# else:
		# 	startY = (height - width) // 2
		# 	rateY = (height - startY * 2) // 6
		# 	startY += shift
		#
		# 	startX = padding
		# 	rateX = (width - startX * 2) // 6
		
		colorChangeButton = {
			"init": ColorEnums.TILE_ORANGE,
			"hover": ColorEnums.TILE_LIGHT_ORANGE
		}
		
		for i in range(6):
			for j in range(6):
				row = i+1
				col = j+1
				
				GUIObject = GUIObjectClass(
					self.__screen,
					startX + (i*rateX), startY + (j*rateY),
					rateX-spaceBetween, rateY-spaceBetween,
					border_radius=2
				)
				
				GUIObject.beButton(color=ColorEnums.TILE_ORANGE)
				GUIObject.makeShadow(offset=3)
				
				dictionary = {
					"Object": GUIObject,
					"row": row,
					"col": col
				}
				
				self.__GameButtons.append(dictionary)
				
				# it's easy to unbind it, as we look for event with id row:col (51 => row 5, col 1)
				self.__bindButton(GUIObject, "Game", row*10 + col, self.__makeMove, [row, col], extraArgsHover=colorChangeButton)
		
		
		# back button
		self.__BackButton = GUIObjectClass(
			self.__screen,
			5, height + 10, startX-20, startX/3.5
		)
		
		self.__BackButton.beButton()
		self.__BackButton.beText(self.__textfont, "Back")
		self.__BackButton.makeShadow(offset=5)
		
		# ID = -10 is for events that won't ever be unbinded
		self.__bindButton(self.__BackButton, "Game", -10, self.__changeState, ["Main Menu"], extraArgsHover={
			# this is the color change dictionary
			"init": ColorEnums.LIGHT_GREEN,
			"hover": ColorEnums.LIGHTER_GREEN
		})
		
		# score
		scoreWidth = 200
		self.__ScoreText = GUIObjectClass(
			self.__screen,
			width//2 - scoreWidth//2 + shiftRight/1.6, 5, scoreWidth, startY - 10
		)
		
		self.__ScoreText.beText(self.__creditsfont, str(self.__score[0]) + " : " + str(self.__score[1]), color=ColorEnums.WHITE)
		self.__ScoreText.makeTextShadow(offset=3)
		
		# win / lose
		OutcomeWidth, OutcomeHeight = 400, 100
		
		# win
		self.__WinLabel = GUIObjectClass(
			self.__screen,
			width//2 - OutcomeWidth//2 + shiftRight/1.6, height//2 - OutcomeHeight//2 + shiftDown/1.1, OutcomeWidth, OutcomeHeight,
			border_radius=1000  # round label
		)
		
		self.__WinLabel.beButton(color=ColorEnums.WINNING_BLUE)
		self.__WinLabel.beText(self.__outcomefont, "You won!")
		self.__WinLabel.makeShadow(offset=5)
	
		# lose
		self.__LoseLabel = GUIObjectClass(
			self.__screen,
			width//2 - OutcomeWidth//2 + shiftRight/1.6, height//2 - OutcomeHeight//2 + shiftDown/1.1, OutcomeWidth, OutcomeHeight,
			border_radius=1000 # round label
		)
		
		self.__LoseLabel.beButton(color=ColorEnums.LOSING_RED)
		self.__LoseLabel.beText(self.__outcomefont, "You lost.")
		self.__LoseLabel.makeShadow(offset=5)
		
		
	def __renderGame(self):
		# background
		self.__screen.fill(ColorEnums.BACKGROUND)
		
		self.__BackButton.render()
		self.__ScoreText.render()
		
		for buttonDict in self.__GameButtons:
			buttonDict["Object"].render()
		
		if self.__gameState == "won":
			self.__WinLabel.render()
		elif self.__gameState == "lost":
			self.__LoseLabel.render()
	# ----
	
	# MAIN MENU
	def __initMainMenu(self):
		# initializing main menu GUI
		
		colorChange = {
			"init": ColorEnums.LIGHT_GREEN,
			"hover": ColorEnums.LIGHTER_GREEN
		}
		
		# buttons
		ButtonProp = {
			"Start1": {
				"Args": [self.__startGame, [True]],
				"Message": "Start (You move first)",
			},
			# I need ("Game") to remain tuple but apparently tuples with just 1 element get converted to just the element
			"Start2": {
				"Args": [self.__startGame, [False]],
				"Message": "Start (AI moves first)",
			},
			"Exit": {
				"Args": [self.__quitGame, []],
				"Message": "Exit Game",
			},
		}
		
		count = 3
		for name in ButtonProp:
			GUIObject = GUIObjectClass(
				self.__screen,
				self.__screen_size["width"] // 4,
				self.__screen_size["height"] * count / 6,
				self.__screen_size["width"] // 2,
				self.__screen_size["height"] // 8,
			)
			count += .9 # used so that objects aren't on top of each other
			
			dictionary = {
				"Name": name,
				"Object": GUIObject
			}
			
			GUIObject.beButton()
			GUIObject.beText(self.__textfont, ButtonProp[name]["Message"])
			GUIObject.makeShadow(offset=6)
			
			self.__MainMenuButtons.append(dictionary)
												# *ButtonProp[name]["Args"] is func and extraArgsFunc
			self.__bindButton(GUIObject, "Main Menu", -10, *ButtonProp[name]["Args"], extraArgsHover=colorChange)
		
		
		# title and credits Texts
		self.__MainMenuTitle = GUIObjectClass(
			self.__screen,
			self.__screen_size["width"] // 2,
			self.__screen_size["height"] * 1 / 6,
			0, 0  # the font sets these
		)
		self.__Credits = GUIObjectClass(
			self.__screen,
			self.__screen_size["width"] // 1.5,
			self.__screen_size["height"] * 1.9 / 6,
			0, 0  # the font sets these
		)
		
		self.__MainMenuTitle.beText(self.__titlefont, "Obstruction", color=ColorEnums.TITLE_PURPLE)
		self.__MainMenuTitle.makeTextShadow(offset=6)
		
		self.__Credits.beText(self.__creditsfont, "project by Ban Mihai from 911", color=ColorEnums.CREDITS_PURPLE)
		self.__Credits.makeTextShadow(offset=2)
	
	
	def __renderMainMenu(self):
		# background
		self.__screen.fill(ColorEnums.BACKGROUND)
		
		self.__MainMenuTitle.render()
		self.__Credits.render()
		
		for buttonDict in self.__MainMenuButtons:
			buttonDict["Object"].render()
	# ----
	
	def __unbind(self, ID):
		# unbinds all events with the given ID
		
		i = 0
		while i < len(self.__Events):
			if self.__Events[i]["ID"] == ID:
				self.__Events.pop(i)
			else:
				i += 1
	
	def __bindButton(self, button, state, ID, func, extraArgsClick=None, extraArgsHover=None):
		"""
		Binds click and hover events for a given button
		:param button: the button
		:param state: the state ("Main Menu" / "Game") so that the event only activates when the game is in this state
		:param ID: the id of the bind, so that it can be unbinded (ID=-10 for events that won't ever be unbinded)
		:param func: the function that should be called after being clicked
		:param extraArgsClick: the arguments of the click function
		:param extraArgsHover: the arguments of the hover function
		"""
		
		self.__Events.append({
			"State": state,
			"ID": ID,  # ID=-10 for events that won't ever be unbinded
			"Type": pygame.MOUSEBUTTONDOWN,
			"Func": self.__clickedButton,
			"Args": [button.x, button.y, button.width, button.height, func, extraArgsClick]
		})
		
		self.__Events.append({
			"State": state,
			"ID": ID,  # ID=-10 for events that won't ever be unbinded
			"Type": pygame.MOUSEMOTION,
			"Func": self.__hoveredButton,
			"Args": [button, button.x, button.y, button.width, button.height, extraArgsHover]
		})
	
	def __handleEvents(self):
		# this handles all events, adding a new event to the self.__Events list will bind it (make it take effect during next events)
		# removing an event from the list will unbind it
		for event in pygame.event.get():
			for eventFuncs in self.__Events:
				if ("State" not in eventFuncs or eventFuncs["State"] == self.__state) and eventFuncs["Type"] == event.type:
					if "Args" in eventFuncs:
						# same as many lines above, this warning is dumb and should disappear
						eventFuncs["Func"](*eventFuncs["Args"])
					else:
						eventFuncs["Func"]()
		
		self.__ColorEnums.update()
		self.__justChangedState = False
	
	
	def start(self):
		while self.__running:
			try:
				if self.__state == "Main Menu":
					self.__renderMainMenu()
				elif self.__state == "Game":
					self.__renderGame()
				
				# events should be handled before display (such as button presses)
				self.__handleEvents()
				
				pygame.display.flip()
			except (DomainError, ServicesError, UIError, SoundError) as err:
				print(err)
	
	
	# defining all event functions here
	def __quitGame(self):
		self.__running = False
	
	
	def __clickedButton(self, xPos: int, yPos: int, width: int, height: int, whatToDoFunc, extraArgs: list = ()):
		mouse = pygame.mouse.get_pos()
		if xPos <= mouse[0] <= xPos + width and yPos <= mouse[1] <= yPos + height:
			self.__soundManager.playSound("click")
			whatToDoFunc(*extraArgs)
			
	
	def __hoveredButton(self, button: GUIObjectClass, xPos: int, yPos: int, width: int, height: int, colorChange=None):
		mouse = pygame.mouse.get_pos()
		if xPos <= mouse[0] <= xPos + width and yPos <= mouse[1] <= yPos + height:
			if button not in self.__hoveredDebounce:
				self.__hoveredDebounce.append(button)
				
				self.__soundManager.playSound("buttonHover")
				if colorChange:
					button.buttonColor = colorChange["hover"]
		else:
			if button in self.__hoveredDebounce:
				self.__hoveredDebounce.remove(button)
				
				if colorChange:
					button.buttonColor = colorChange["init"]
		
	
	def __startGame(self, HumanStarts: bool):
		self.__gameState = ""
		self.__changeState("Game")
		self.__resetGameGUI()
		self.__service = MainService.MainServiceClass()
		
		if not HumanStarts:
			self.__service.AIFirstMove()
			self.__updateAllTiles()
			
	
	def __changeState(self, newState):
		self.__state = newState
		self.__justChangedState = True
	
	
	def __makeMove(self, row, col):
		if self.__justChangedState:
			return
		
		didHumanWin = self.__service.makeHumanMove(str(row) + " " + str(col))
		
		self.__updateAllTiles()
	
		if self.__service.isGameOver():
			if didHumanWin:
				self.__soundManager.playSound("win")
				self.__gameState = "won"
				self.__score[0] += 1
			else:
				self.__soundManager.playSound("lose")
				self.__gameState = "lost"
				self.__score[1] += 1
			
			self.__ScoreText.beText(self.__creditsfont, str(self.__score[0]) + " : " + str(self.__score[1]), color=ColorEnums.WHITE)
			self.__ScoreText.makeTextShadow(offset=3)
				
				