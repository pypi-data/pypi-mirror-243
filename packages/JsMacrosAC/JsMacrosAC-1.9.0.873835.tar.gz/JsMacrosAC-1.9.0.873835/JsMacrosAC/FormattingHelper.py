from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

net_minecraft_util_Formatting = TypeVar("net_minecraft_util_Formatting")
Formatting = net_minecraft_util_Formatting


class FormattingHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: Formatting) -> None:
		pass

	@overload
	def getColorValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color value of this formatting. 
		"""
		pass

	@overload
	def getColorIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the index of this formatting or '-1' if this formatting is a modifier. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this formatting. 
		"""
		pass

	@overload
	def getCode(self) -> str:
		"""The color code can be used with the paragraph to color text.\n
		Since: 1.8.4 

		Returns:
			the color code of this formatting. 
		"""
		pass

	@overload
	def isColor(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this formatting is a color, 'false' otherwise. 
		"""
		pass

	@overload
	def isModifier(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this formatting is a modifier, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


