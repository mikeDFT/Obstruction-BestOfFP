
import pygame

# part of the GUI, but I want to move it out of that huge script to split things and make everything easier to access

"""
As it's part of the GUI (UI), it doesn't require comments, but I added them so that it's easier to understand what's going on
"""

class ColorEnums:
	# colors to have the centralized and easier to change/use
	
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	
	LIGHT_BLUE = (78, 255, 255)
	LIGHT_GREEN = (138, 255, 165)
	LIGHTER_GREEN = (181, 255, 198)
	
	LOSING_RED = (255, 104, 104)
	WINNING_BLUE = (108, 236, 255)
	
	TITLE_PURPLE = (162, 37, 225)
	CREDITS_PURPLE = (131, 28, 182)
	TEXT_COLOR = (55, 55, 55)
	TILE_ORANGE = (218, 195, 106)
	TILE_LIGHT_ORANGE = (230, 214, 147)
	TILE_LOCKED = (146, 131, 71)
	
	BACKGROUND_COLORS = [  # many new colors can be added, it's made so that it works by just adding them to this list
		# these colors have s=32 v=75 (only the hue is changed)
		(130, 192, 138),  # green
		(130, 159, 192),  # blue
		(165, 130, 192),  # purple
		(192, 165, 130),  # orange
	]
	BACKGROUND = None
	
	def __init__(self):
		ColorEnums.BACKGROUND = ColorEnums.BACKGROUND_COLORS[0]
		self.cycleDuration = 2000  # in milliseconds
		self.__alpha = 0
		self.__direction = 0
	
	@staticmethod
	def __lerp(a, b, alpha):  # linear number interpolation
		return a + (b - a) * alpha
	
	def __lerpColor(self, c1, c2, alpha):
		# linear interpolation of colors (tuples with 3 numerical values)
		
		cOut = []
		for i in range(3):
			cOut.append(self.__lerp(c1[i], c2[i], alpha))
		
		return tuple(cOut)
	
	def update(self):
		# update the BACKGROUND, interpolating between the given BACKGROUND_COLORS depending on
		# pygame.time.get_ticks() (time in ms since pygame was initialized)
		
		ms = pygame.time.get_ticks()
		# direction is basically the current color from which we interpolate to the next one in the list
		self.__direction = (ms // self.cycleDuration) % len(ColorEnums.BACKGROUND_COLORS)
		# alpha is a float value between 0 and 1 which represents how far from the 1st color we are to the 2nd one
		# alpha = 0 -> c1 ; alpha = 0.5 -> half way ; alpha = 1 -> c2
		self.__alpha = (ms % self.cycleDuration) / self.cycleDuration
		
		# lerping using the function
		ColorEnums.BACKGROUND = self.__lerpColor(
			ColorEnums.BACKGROUND_COLORS[self.__direction],
			ColorEnums.BACKGROUND_COLORS[(self.__direction + 1) % len(ColorEnums.BACKGROUND_COLORS)],
			self.__alpha
		)
		