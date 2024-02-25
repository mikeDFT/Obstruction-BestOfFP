
class ServicesError(Exception):
	def __init__(self, message):
		self.__message = message
	
	def __str__(self):
		return "[ServicesError]" + str(self.__message)

