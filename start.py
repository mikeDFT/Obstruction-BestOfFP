
from jproperties import Properties

from ui.Console import ConsoleClass
from ui.GUI import GUIClass

"""
Notes:
	- Implemented:
		AI - minimax algorithm:
			Uses alpha, beta pruning (removes branches that don't need to be computed)
			It's made so that if it's winning, it's winning as soon as possible
				and if it's losing, it's losing as late as possible
				(giving the human more opportunities to make a mistake)
			Uses caching when there are over 20 (by default) available moves as that takes a
				long time to compute and not a lot of memory used
			First move (when AI starts) would normally be in the left upper corner, but since
				the board can be rotated all corners are the same, so to not make it boring,
				the corner is randomly chosen
			It creates the cache in real time, if there isn't a move cached already and there are
				20+ available moves in that position, it saved the move into the cache
			There's an optimized board created for minimax to make it even faster
			== The first one to move can always win, there is 0 chance of you winning if AI starts
				best play is to keep moving in the corner of the board and only take 4 squares until
				someone breaks the loop
		
		GUI - with pygame:
			I made GUIObjectClass for text and/or button (and textshadow, buttonshadow) - very easy to use
			There's an events list with all the events and the functions binded so that it's easy
				to bind/unbind events
			Colors use enums. A centralized class with all enums. It's easy to change them this way
			RGB changing background, many more colors can be added to the list as it's made to work that way
				(uses lerping - linear interpolation of numbers [a - (b-a) * alpha],
				I wrote a post at some point explain this)
			Added window name and icon (icon made by myself)
			
			
		Sounds Manager - made by myself:
			credits for each sound in the py script (all sounds are under CC0 license, except for music, music is under Attribution 4.0)
			played them using pygame
"""


if __name__ == "__main__":
	"""
	Starts up the application
	"""
	
	settings = Properties()
	file = open("files/settings.properties", "rb")
	settings.load(file)
	
	UIType = settings.get("UIType").data
	
	if UIType == "GUI":
		myUI = GUIClass()
		myUI.start()
	elif UIType == "Console":
		myUI = ConsoleClass()
		myUI.start()
