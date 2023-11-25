from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .FormattingHelper import FormattingHelper
from .TextHelper import TextHelper

net_minecraft_entity_boss_BossBar = TypeVar("net_minecraft_entity_boss_BossBar")
BossBar = net_minecraft_entity_boss_BossBar


class BossBarHelper(BaseHelper):
	"""
	Since: 1.2.1 
	"""

	@overload
	def __init__(self, b: BossBar) -> None:
		pass

	@overload
	def getUUID(self) -> str:
		"""
		Since: 1.2.1 

		Returns:
			boss bar uuid. 
		"""
		pass

	@overload
	def getPercent(self) -> float:
		"""
		Since: 1.2.1 

		Returns:
			percent of boss bar remaining. 
		"""
		pass

	@overload
	def getColor(self) -> str:
		"""
		Since: 1.2.1 

		Returns:
			boss bar color. 
		"""
		pass

	@overload
	def getStyle(self) -> str:
		"""
		Since: 1.2.1 

		Returns:
			boss bar notch style. 
		"""
		pass

	@overload
	def getColorValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of this boss bar. 
		"""
		pass

	@overload
	def getColorFormat(self) -> FormattingHelper:
		"""
		Since: 1.8.4 

		Returns:
			the format of the boss bar's color. 
		"""
		pass

	@overload
	def getName(self) -> TextHelper:
		"""
		Since: 1.2.1 

		Returns:
			name of boss bar 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


