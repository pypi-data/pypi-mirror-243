from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .EnchantmentHelper import EnchantmentHelper
from .TextHelper import TextHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper
from .BlockHelper import BlockHelper
from .BlockStateHelper import BlockStateHelper
from .CreativeItemStackHelper import CreativeItemStackHelper
from .ItemHelper import ItemHelper

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class ItemStackHelper(BaseHelper):
	"""
	"""

	@overload
	def __init__(self, id: str, count: int) -> None:
		pass

	@overload
	def __init__(self, i: ItemStack) -> None:
		pass

	@overload
	def setDamage(self, damage: int) -> "ItemStackHelper":
		"""Sets the item damage value.
You should use CreativeItemStackHelper#setDamage(int) instead.
You may want to use ItemStackHelper#copy() first.\n
		Since: 1.2.0 

		Args:
			damage: 

		Returns:
			self 
		"""
		pass

	@overload
	def isDamageable(self) -> bool:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def isUnbreakable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item is unbreakable, 'false' otherwise. 
		"""
		pass

	@overload
	def isEnchantable(self) -> bool:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def isEnchanted(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the item is enchanted, 'false' otherwise. 
		"""
		pass

	@overload
	def getEnchantments(self) -> List[EnchantmentHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all enchantments on this item. 
		"""
		pass

	@overload
	def getEnchantment(self, id: str) -> EnchantmentHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the id of the enchantment to check for 

		Returns:
			the enchantment instance, containing the level, or 'null' if the item is not
enchanted with the specified enchantment. 
		"""
		pass

	@overload
	def canBeApplied(self, enchantment: EnchantmentHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check for 

		Returns:
			'true' if the specified enchantment can be applied to this item, 'false' otherwise. 
		"""
		pass

	@overload
	def hasEnchantment(self, enchantment: EnchantmentHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to check for 

		Returns:
			'true' if the item is enchanted with the specified enchantment of the same
level, 'false' otherwise. 
		"""
		pass

	@overload
	def hasEnchantment(self, enchantment: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			enchantment: the id of the enchantment to check for 

		Returns:
			'true' if the item is enchanted with the specified enchantment, 'false' otherwise. 
		"""
		pass

	@overload
	def getPossibleEnchantments(self) -> List[EnchantmentHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all enchantments that can be applied to this item. 
		"""
		pass

	@overload
	def getPossibleEnchantmentsFromTable(self) -> List[EnchantmentHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all enchantments that can be applied to this item through an enchanting table. 
		"""
		pass

	@overload
	def getLore(self) -> List[TextHelper]:
		"""The returned list is a copy of the original list and can be modified without affecting the
original item. For editing the actual lore see CreativeItemStackHelper#addLore(java.lang.Object...) .\n
		Since: 1.8.4 

		Returns:
			a list of all lines of lore on this item. 
		"""
		pass

	@overload
	def getMaxDurability(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum durability of this item. 
		"""
		pass

	@overload
	def getDurability(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current durability of this item. 
		"""
		pass

	@overload
	def getRepairCost(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current repair cost of this item. 
		"""
		pass

	@overload
	def getDamage(self) -> int:
		"""

		Returns:
			the damage taken by this item. 
		"""
		pass

	@overload
	def getMaxDamage(self) -> int:
		"""

		Returns:
			the maximum damage this item can take. 
		"""
		pass

	@overload
	def getAttackDamage(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the default attack damage of this item. 
		"""
		pass

	@overload
	def getDefaultName(self) -> TextHelper:
		"""
		Since: 1.2.0 

		Returns:
			was string before 1.6.5 
		"""
		pass

	@overload
	def getName(self) -> TextHelper:
		"""

		Returns:
			was string before 1.6.5 
		"""
		pass

	@overload
	def getCount(self) -> int:
		"""

		Returns:
			the item count this stack is holding. 
		"""
		pass

	@overload
	def getMaxCount(self) -> int:
		"""

		Returns:
			the maximum amount of items this stack can hold. 
		"""
		pass

	@overload
	def getNBT(self) -> NBTElementHelper_NBTCompoundHelper:
		"""
		Since: 1.1.6, was a String until 1.5.1 
		"""
		pass

	@overload
	def getCreativeTab(self) -> List[TextHelper]:
		"""
		Since: 1.1.3 
		"""
		pass

	@overload
	def getItemID(self) -> str:
		"""
		"""
		pass

	@overload
	def getItemId(self) -> str:
		"""
		Since: 1.6.4 
		"""
		pass

	@overload
	def getTags(self) -> List[str]:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def isFood(self) -> bool:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def isTool(self) -> bool:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def isWearable(self) -> bool:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def getMiningLevel(self) -> int:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def isEmpty(self) -> bool:
		"""
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def equals(self, ish: "ItemStackHelper") -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			ish: 
		"""
		pass

	@overload
	def equals(self, is_: ItemStack) -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			is: 
		"""
		pass

	@overload
	def isItemEqual(self, ish: "ItemStackHelper") -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			ish: 
		"""
		pass

	@overload
	def isItemEqual(self, is_: ItemStack) -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			is: 
		"""
		pass

	@overload
	def isItemEqualIgnoreDamage(self, ish: "ItemStackHelper") -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			ish: 
		"""
		pass

	@overload
	def isItemEqualIgnoreDamage(self, is_: ItemStack) -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			is: 
		"""
		pass

	@overload
	def isNBTEqual(self, ish: "ItemStackHelper") -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			ish: 
		"""
		pass

	@overload
	def isNBTEqual(self, is_: ItemStack) -> bool:
		"""
		Since: 1.1.3 [citation needed] 

		Args:
			is: 
		"""
		pass

	@overload
	def isOnCooldown(self) -> bool:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getCooldownProgress(self) -> float:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def isSuitableFor(self, block: BlockHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			block: the block to check 

		Returns:
			'true' if the given block can be mined and drops when broken with this item, 'false' otherwise. 
		"""
		pass

	@overload
	def isSuitableFor(self, block: BlockStateHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			block: the block to check 

		Returns:
			'true' if the given block can be mined and drops when broken with this item, 'false' otherwise. 
		"""
		pass

	@overload
	def getCreative(self) -> CreativeItemStackHelper:
		"""CreativeItemStackHelper adds methods for manipulating the item's nbt data.\n
		Since: 1.8.4 

		Returns:
			a CreativeItemStackHelper instance for this item. 
		"""
		pass

	@overload
	def getItem(self) -> ItemHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item this stack is made of. 
		"""
		pass

	@overload
	def copy(self) -> "ItemStackHelper":
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def hasDestroyRestrictions(self) -> bool:
		"""This flag only affects players in adventure mode and makes sure only specified blocks can be
destroyed by this item.\n
		Since: 1.8.4 

		Returns:
			'true' if the can destroy flag is set, 'false' otherwise. 
		"""
		pass

	@overload
	def hasPlaceRestrictions(self) -> bool:
		"""This flag only affects players in adventure mode and makes sure this item can only be placed
on specified blocks.\n
		Since: 1.8.4 

		Returns:
			'true' if the can place on flag is set, 'false' otherwise. 
		"""
		pass

	@overload
	def getDestroyRestrictions(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all filters set for the can destroy flag. 
		"""
		pass

	@overload
	def getPlaceRestrictions(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all filters set for the can place on flag. 
		"""
		pass

	@overload
	def areEnchantmentsHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if enchantments are hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def areModifiersHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if modifiers are hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def isUnbreakableHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the unbreakable flag is hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def isCanDestroyHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the can destroy flag is hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def isCanPlaceHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the can place flag is hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def areAdditionalsHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if additional attributes are hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def isDyeHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if dye of colored leather armor is hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def areNbtEqual(self, left: ItemStack, right: ItemStack) -> bool:
		"""The old implementation use used in ItemStack before 1.20. This only checks for the nbt data, the
items themselves are not compared.

		Args:
			left: the first item stack 
			right: the second item stack 

		Returns:
			'true' if the two item stacks have equal nbt data, 'false' otherwise. 
		"""
		pass

	pass


