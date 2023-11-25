from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .ItemHelper import ItemHelper
from .ItemStackHelper import ItemStackHelper

net_minecraft_enchantment_Enchantment = TypeVar("net_minecraft_enchantment_Enchantment")
Enchantment = net_minecraft_enchantment_Enchantment


class EnchantmentHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: Enchantment) -> None:
		pass

	@overload
	def __init__(self, base: Enchantment, level: int) -> None:
		pass

	@overload
	def __init__(self, enchantment: str) -> None:
		pass

	@overload
	def getLevel(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the level of this enchantment. 
		"""
		pass

	@overload
	def getMinLevel(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the minimum possible level of this enchantment that one can get in vanilla. 
		"""
		pass

	@overload
	def getMaxLevel(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum possible level of this enchantment that one can get in vanilla. 
		"""
		pass

	@overload
	def getLevelName(self, level: int) -> str:
		"""
		Since: 1.8.4 

		Args:
			level: the level for the name 

		Returns:
			the translated name of this enchantment for the given level. 
		"""
		pass

	@overload
	def getRomanLevelName(self) -> TextHelper:
		"""Because roman numerals only support positive integers in the range of 1 to 3999, this method
will return the arabic numeral for any given level outside that range.\n
		Since: 1.8.4 

		Returns:
			the translated name of this enchantment for the given level in roman numerals. 
		"""
		pass

	@overload
	def getRomanLevelName(self, level: int) -> TextHelper:
		"""Because roman numerals only support positive integers in the range of 1 to 3999, this method
will return the arabic numeral for any given level outside that range.\n
		Since: 1.8.4 

		Args:
			level: the level for the name 

		Returns:
			the translated name of this enchantment for the given level in roman numerals. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this enchantment. 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the id of this enchantment. 
		"""
		pass

	@overload
	def getRarity(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the rarity of this enchantment. 
		"""
		pass

	@overload
	def getConflictingEnchantments(self) -> List["EnchantmentHelper"]:
		"""Only accounts for enchantments of the same target type.\n
		Since: 1.8.4 

		Returns:
			a list of all enchantments that conflict with this one. 
		"""
		pass

	@overload
	def getConflictingEnchantments(self, ignoreType: bool) -> List["EnchantmentHelper"]:
		"""
		Since: 1.8.4 

		Args:
			ignoreType: whether to check only enchantments that can be applied to the same target
                  type. 

		Returns:
			a list of all enchantments that conflict with this one. 
		"""
		pass

	@overload
	def getCompatibleEnchantments(self) -> List["EnchantmentHelper"]:
		"""Only accounts for enchantments of the same target type.\n
		Since: 1.8.4 

		Returns:
			a list of all enchantments that can be combined with this one. 
		"""
		pass

	@overload
	def getCompatibleEnchantments(self, ignoreType: bool) -> List["EnchantmentHelper"]:
		"""
		Since: 1.8.4 

		Args:
			ignoreType: whether to check only enchantments that can be applied to the same target
                  type. 

		Returns:
			a list of all enchantments that can be combined with this one. 
		"""
		pass

	@overload
	def getTargetType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the type of item this enchantment is compatible with. 
		"""
		pass

	@overload
	def getWeight(self) -> int:
		"""The weight of an enchantment is bound to its rarity. The higher the weight, the more likely
it is to be chosen.\n
		Since: 1.8.4 

		Returns:
			the relative probability of this enchantment being applied to an enchanted item
through the enchanting table or a loot table. 
		"""
		pass

	@overload
	def isCursed(self) -> bool:
		"""Curses are enchantments that can't be removed from the item they were applied to. They
usually only have one possible level and can't be upgraded. When combining items with curses
on them, they are transferred like any other enchantment. They can't be obtained through
enchantment tables, but rather from loot chests, fishing or trading with villagers.\n
		Since: 1.8.4 

		Returns:
			'true' if this enchantment is a curse, 'false' otherwise. 
		"""
		pass

	@overload
	def isTreasure(self) -> bool:
		"""Treasures are enchantments that can't be obtained through enchantment tables, but rather from
loot chests, fishing or trading with villagers.\n
		Since: 1.8.4 

		Returns:
			'true' if this enchantment is a treasure, 'false' otherwise. 
		"""
		pass

	@overload
	def canBeApplied(self, item: ItemHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check 

		Returns:
			'true' if this enchantment can be applied to the given item type, 'false' otherwise. 
		"""
		pass

	@overload
	def canBeApplied(self, item: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check 

		Returns:
			'true' if this enchantment can be applied to the given item, 'false' otherwise. 
		"""
		pass

	@overload
	def getAcceptableItems(self) -> List[ItemHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all acceptable item ids for this enchantment. 
		"""
		pass

	@overload
	def isCompatible(self, enchantment: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check 

		Returns:
			'true' if this enchantment is compatible with the given enchantment, 'false' otherwise. 
		"""
		pass

	@overload
	def isCompatible(self, enchantment: "EnchantmentHelper") -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check 

		Returns:
			'true' if this enchantment is compatible with the given enchantment, 'false' otherwise. 
		"""
		pass

	@overload
	def conflictsWith(self, enchantment: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check 

		Returns:
			'true' if this enchantment conflicts with the given enchantment, 'false' otherwise. 
		"""
		pass

	@overload
	def conflictsWith(self, enchantment: "EnchantmentHelper") -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check 

		Returns:
			'true' if this enchantment conflicts with the given enchantment, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	pass


