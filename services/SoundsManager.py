
import pygame

# this is part of the GUI

"""
all sound effects are under CC0 license
here's the links:
win - https://freesound.org/people/Leszek_Szary/sounds/171671/
lose - https://freesound.org/people/TaranP/sounds/362204/
click - https://freesound.org/people/kwahmah_02/sounds/256116/
buttonHover - https://freesound.org/people/Fachii/sounds/338229/

the music is under Attribution 4.0 license:
music_electro: https://freesound.org/people/frankum/sounds/384468/
music_sandbox: https://freesound.org/people/Unlistenable/sounds/416778/  (Attribution NonCommercial 4.0)
"""

class SoundError(Exception):
	def __init__(self, message):
		self.__message = message
	
	def __str__(self):
		return "[SoundError]: " + str(self.__message)


class SoundManagerClass:
	def __init__(self, soundsPath: str = "sounds/"):
		# soundsPath is relative to the file that imports this class
		# so when doing unittests, it's different
		
		# if the sound is too loud/quiet, depending on the noise around
		soundScale = 1.2
		
		self.__musicName = "music_electro"
		
		# dictionary with sound data
		self.__soundsData = {
			"click": {
				"name": "click.wav",
				"volume": .2 * soundScale
			},
			"buttonHover": {
				"name": "buttonHover.wav",
				"volume": .4 * soundScale
			},
			"lose": {
				"name": "lose.wav",
				"volume": .4 * soundScale
			},
			"win": {
				"name": "win.wav",
				"volume": .3 * soundScale
			},
			"music_sandbox": {
				"name": "music_sandbox.wav",
				"volume": .2 * soundScale
			},
			"music_electro": {
				"name": "music_electro.mp3",
				"volume": .15 * soundScale
			},
		}
		
		self.__sounds = {}
		
		# loading all sounds
		for name in self.__soundsData:
			self.__sounds[name] = pygame.mixer.Sound(soundsPath + self.__soundsData[name]["name"])
			self.__sounds[name].set_volume(self.__soundsData[name]["volume"])
		
		# initializing music
		self.__initMusic()
		
	
	def __initMusic(self):
		self.playSound(self.__musicName, -1)
	
	
	# not using loops anyway, there's no music
	def playSound(self, name: str, loops: int = 0):  # loops = 0 means it will play once
		"""
		plays a sound
		:param name: name of sound
		:param loops: nr of loops + 1 (-1 = infinite)
		"""
		
		if name not in self.__sounds:
			raise SoundError("Sound not found")
		
		pygame.mixer.Sound.play(self.__sounds[name], loops=loops)
		
		