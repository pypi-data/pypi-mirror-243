from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .MethodWrapper import MethodWrapper

java_util_regex_Pattern = TypeVar("java_util_regex_Pattern")
Pattern = java_util_regex_Pattern

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class TextHelper(BaseHelper):
	"""
	Since: 1.0.8 
	"""
	STRIP_FORMATTING_PATTERN: Pattern

	@overload
	def wrap(self, t: Text) -> "TextHelper":
		pass

	@overload
	def replaceFromJson(self, json: str) -> "TextHelper":
		"""replace the text in this class with JSON data.\n
		Since: 1.0.8 

		Args:
			json: 
		"""
		pass

	@overload
	def replaceFromString(self, content: str) -> "TextHelper":
		"""replace the text in this class with String data.\n
		Since: 1.0.8 

		Args:
			content: 
		"""
		pass

	@overload
	def getJson(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			JSON data representation. 
		"""
		pass

	@overload
	def getString(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			the text content. 
		"""
		pass

	@overload
	def getStringStripFormatting(self) -> str:
		"""
		Since: 1.6.5 

		Returns:
			the text content. stripped formatting when servers send it the (super) old way due to shitty coders. 
		"""
		pass

	@overload
	def withoutFormatting(self) -> "TextHelper":
		"""
		Since: 1.8.4 

		Returns:
			the text helper without the formatting applied. 
		"""
		pass

	@overload
	def visit(self, visitor: MethodWrapper) -> "TextHelper":
		"""
		Since: 1.6.5 

		Args:
			visitor: function with 2 args, no return. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of this text. 
		"""
		pass

	@overload
	def toJson(self) -> str:
		"""
		Since: 1.0.8 
		"""
		pass

	@overload
	def toString(self) -> str:
		"""
		Since: 1.0.8, this used to do the same as TextHelper#getString() 

		Returns:
			String representation of text helper. 
		"""
		pass

	pass


