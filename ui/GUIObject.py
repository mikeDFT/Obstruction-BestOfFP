
import pygame
from ui.ColorEnums import ColorEnums
from ui import UIError

# part of the GUI, but I want to move it out of that huge script to split things and make everything easier to access

"""
As it's part of the GUI (UI), it doesn't require comments, but I added them so that it's easier to understand what's going on
"""

class GUIObjectClass:
	# GUI object to easily create text / buttons / buttons w text
	
	def __init__(self, screen, xPos, yPos, width, height, border_radius=7):
		self.__screen = screen
		self.x = xPos
		self.y = yPos
		self.width = width
		self.height = height
		self.border_radius = border_radius
		
		self.buttonColor = ColorEnums.LIGHT_GREEN
		self.__button = None
		self.__text = None
		self.__buttonShadow = None
		self.__textShadow = None
		
		# for text shadow
		self.__textShadowOffset = None
		self.__font = None
		self.__message = None
	
	def beButton(self, color=ColorEnums.LIGHT_GREEN):
		# can be called to create the button
		
		self.buttonColor = color
		self.__button = pygame.Rect(self.x, self.y, self.width, self.height)
	
	def beText(self, font, message, color=ColorEnums.TEXT_COLOR):
		# can be called to create the text
		
		# can also be called to change the current message/font/color
		self.__font = font
		self.__message = message
		self.__text = font.render(message, True, color)
	
	def makeShadow(self, offset=8):
		# adds shadow to button
		
		if self.__button:
			self.__buttonShadow = pygame.Rect(self.x + offset, self.y + offset, self.width, self.height)
		else:
			raise UIError("No button object for shadow")
	
	def makeTextShadow(self, offset=4):
		# adds shadow to text
		
		if self.__text:
			self.__textShadowOffset = offset
			self.__textShadow = self.__font.render(self.__message, True, ColorEnums.BLACK)
		else:
			raise UIError("No text object for shadow")
	
	def __centerText(self, text, centerX, centerY):
		# centers text in the middle of the object
		
		center = text.get_rect(center=(centerX, centerY))
		self.__screen.blit(text, center)
	
	def render(self):
		# renders the button, the text and the shadows for both
		# shadow rendered first so that the object can be rendered on top
		
		if self.__button:
			if self.__buttonShadow:
				pygame.draw.rect(self.__screen, ColorEnums.BLACK, self.__buttonShadow, border_radius=self.border_radius)
			
			pygame.draw.rect(self.__screen, self.buttonColor, self.__button, border_radius=self.border_radius)
		
		if self.__text:
			if self.__textShadow:
				self.__centerText(
					self.__textShadow,
					self.x + self.width // 2 + self.__textShadowOffset,
					self.y + self.height // 2 + self.__textShadowOffset
				)
			
			self.__centerText(
				self.__text,
				self.x + self.width // 2,
				self.y + self.height // 2
			)
			