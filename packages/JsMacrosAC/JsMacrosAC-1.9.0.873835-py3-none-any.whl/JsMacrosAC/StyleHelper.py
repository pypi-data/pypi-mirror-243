from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .FormattingHelper import FormattingHelper

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable

net_minecraft_text_Style = TypeVar("net_minecraft_text_Style")
Style = net_minecraft_text_Style


class StyleHelper(BaseHelper):
	"""
	Since: 1.6.5 
	"""

	@overload
	def __init__(self, base: Style) -> None:
		pass

	@overload
	def hasColor(self) -> bool:
		pass

	@overload
	def getColor(self) -> int:
		"""

		Returns:
			the color index of this style or '-1' if no color is set. 
		"""
		pass

	@overload
	def getFormatting(self) -> FormattingHelper:
		"""
		Since: 1.8.4 

		Returns:
			the formatting of this style, or 'null' if no formatting was found. 
		"""
		pass

	@overload
	def getColorIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color index of this style or '-1' if no color is set. 
		"""
		pass

	@overload
	def getColorValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color value of this style or '-1' if it doesn't have one. 
		"""
		pass

	@overload
	def getColorName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the color name of this style or 'null' if it has no color. 
		"""
		pass

	@overload
	def hasCustomColor(self) -> bool:
		pass

	@overload
	def getCustomColor(self) -> int:
		pass

	@overload
	def bold(self) -> bool:
		pass

	@overload
	def italic(self) -> bool:
		pass

	@overload
	def underlined(self) -> bool:
		pass

	@overload
	def strikethrough(self) -> bool:
		pass

	@overload
	def obfuscated(self) -> bool:
		pass

	@overload
	def getClickAction(self) -> str:
		pass

	@overload
	def getClickValue(self) -> str:
		pass

	@overload
	def getCustomClickValue(self) -> Runnable:
		pass

	@overload
	def getHoverAction(self) -> str:
		pass

	@overload
	def getHoverValue(self) -> object:
		pass

	@overload
	def getInsertion(self) -> str:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


