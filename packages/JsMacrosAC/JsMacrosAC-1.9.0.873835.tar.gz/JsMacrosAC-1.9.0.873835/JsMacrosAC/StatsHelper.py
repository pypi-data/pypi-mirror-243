from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper

net_minecraft_stat_StatHandler = TypeVar("net_minecraft_stat_StatHandler")
StatHandler = net_minecraft_stat_StatHandler

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class StatsHelper(BaseHelper):

	@overload
	def __init__(self, base: StatHandler) -> None:
		pass

	@overload
	def getStatList(self) -> List[str]:
		pass

	@overload
	def getStatText(self, statKey: str) -> Text:
		pass

	@overload
	def getRawStatValue(self, statKey: str) -> int:
		pass

	@overload
	def getFormattedStatValue(self, statKey: str) -> str:
		pass

	@overload
	def getFormattedStatMap(self) -> Mapping[str, str]:
		pass

	@overload
	def getRawStatMap(self) -> Mapping[str, int]:
		pass

	@overload
	def getEntityKilled(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the entity 

		Returns:
			how many times the player has killed the entity. 
		"""
		pass

	@overload
	def getKilledByEntity(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the entity 

		Returns:
			how many times the player has killed the specified entity. 
		"""
		pass

	@overload
	def getBlockMined(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the block 

		Returns:
			how many times the player has mined the block. 
		"""
		pass

	@overload
	def getItemBroken(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the item 

		Returns:
			how many times the player has broken the item. 
		"""
		pass

	@overload
	def getItemCrafted(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the item 

		Returns:
			how many times the player has crafted the item. 
		"""
		pass

	@overload
	def getItemUsed(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the item 

		Returns:
			how many times the player has used the item. 
		"""
		pass

	@overload
	def getItemPickedUp(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the item 

		Returns:
			how many times the player has picked up the item. 
		"""
		pass

	@overload
	def getItemDropped(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the item 

		Returns:
			how many times the player has dropped the item. 
		"""
		pass

	@overload
	def getCustomStat(self, id: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the custom stat 

		Returns:
			the value of the custom stat. 
		"""
		pass

	@overload
	def getCustomFormattedStat(self, id: str) -> str:
		"""
		Since: 1.8.4 

		Args:
			id: the identifier of the custom stat 

		Returns:
			the formatted value of the custom stat. 
		"""
		pass

	@overload
	def updateStatistics(self) -> "StatsHelper":
		"""Used to request an update of the statistics from the server.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


