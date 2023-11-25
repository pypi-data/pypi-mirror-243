from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

net_minecraft_util_DyeColor = TypeVar("net_minecraft_util_DyeColor")
DyeColor = net_minecraft_util_DyeColor


class DyeColorHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: DyeColor) -> None:
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the color. 
		"""
		pass

	@overload
	def getId(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color's identifier. 
		"""
		pass

	@overload
	def getColorValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color's rgb value. 
		"""
		pass

	@overload
	def getFireworkColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color's variation when used in fireworks. 
		"""
		pass

	@overload
	def getSignColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color's variation when used on signs. 
		"""
		pass

	pass


