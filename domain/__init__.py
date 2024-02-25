
class DomainError(Exception):
	def __init__(self, message):
		self.__message = message
	
	def __str__(self):
		return "[DomainError]" + str(self.__message)

