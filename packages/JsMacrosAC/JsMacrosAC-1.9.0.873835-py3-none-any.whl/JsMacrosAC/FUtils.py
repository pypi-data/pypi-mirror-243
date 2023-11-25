from typing import overload
from typing import List
from .BaseLibrary import BaseLibrary
from .TextHelper import TextHelper


class FUtils(BaseLibrary):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def openUrl(self, url: str) -> None:
		"""
		Since: 1.8.4 

		Args:
			url: the url to open 
		"""
		pass

	@overload
	def openFile(self, path: str) -> None:
		"""
		Since: 1.8.4 

		Args:
			path: the path top open, relative the config folder 
		"""
		pass

	@overload
	def copyToClipboard(self, text: str) -> None:
		"""Copies the text to the clipboard.\n
		Since: 1.8.4 

		Args:
			text: the text to copy 
		"""
		pass

	@overload
	def getClipboard(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the text from the clipboard. 
		"""
		pass

	@overload
	def guessName(self, text: TextHelper) -> str:
		"""Tries to guess the name of the sender of a given message. This is not guaranteed to work and
for specific servers it may be better to use regex instead.\n
		Since: 1.8.4 

		Args:
			text: the text to check 

		Returns:
			the name of the sender or 'null' if it couldn't be guessed. 
		"""
		pass

	@overload
	def guessName(self, text: str) -> str:
		"""Tries to guess the name of the sender of a given message. This is not guaranteed to work and
for specific servers it may be better to use regex instead.\n
		Since: 1.8.4 

		Args:
			text: the text to check 

		Returns:
			the name of the sender or 'null' if it couldn't be guessed. 
		"""
		pass

	@overload
	def guessNameAndRoles(self, text: TextHelper) -> List[str]:
		"""Tries to guess the name, as well as the titles and roles of the sender of the given message.
This is not guaranteed to work and for specific servers it may be better to use regex
instead.\n
		Since: 1.8.4 

		Args:
			text: the text to check 

		Returns:
			a list of names, titles and roles of the sender or an empty list if it couldn't be
guessed. 
		"""
		pass

	@overload
	def guessNameAndRoles(self, text: str) -> List[str]:
		"""Tries to guess the name, as well as the titles and roles of the sender of the given message.
This is not guaranteed to work and for specific servers it may be better to use regex
instead.\n
		Since: 1.8.4 

		Args:
			text: the text to check 

		Returns:
			a list of names, titles and roles of the sender or an empty list if it couldn't be
guessed. 
		"""
		pass

	@overload
	def hashString(self, message: str) -> str:
		"""Hashes the given string with sha-256.\n
		Since: 1.8.4 

		Args:
			message: the message to hash 

		Returns:
			the hashed message. 
		"""
		pass

	@overload
	def hashString(self, message: str, algorithm: str) -> str:
		"""Hashes the given string with sha-256 the selected algorithm.\n
		Since: 1.8.4 

		Args:
			message: the message to hash 
			algorithm: sha1 | sha256 | sha384 | sha512 | md2 | md5 

		Returns:
			the hashed message. 
		"""
		pass

	@overload
	def encode(self, message: str) -> str:
		"""Encodes the given string with Base64.\n
		Since: 1.8.4 

		Args:
			message: the message to encode 

		Returns:
			the encoded message. 
		"""
		pass

	@overload
	def decode(self, message: str) -> str:
		"""Decodes the given string with Base64.\n
		Since: 1.8.4 

		Args:
			message: the message to decode 

		Returns:
			the decoded message. 
		"""
		pass

	pass


