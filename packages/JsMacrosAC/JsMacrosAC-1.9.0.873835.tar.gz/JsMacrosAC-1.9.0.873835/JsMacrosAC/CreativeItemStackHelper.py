from typing import overload
from typing import List
from typing import TypeVar
from .ItemStackHelper import ItemStackHelper
from .TextHelper import TextHelper
from .EnchantmentHelper import EnchantmentHelper

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class CreativeItemStackHelper(ItemStackHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, itemStack: ItemStack) -> None:
		pass

	@overload
	def setDamage(self, damage: int) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			damage: the damage the item should take 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setDurability(self, durability: int) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			durability: the new durability of this item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCount(self, count: int) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			count: the new count of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setName(self, name: str) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			name: the new name of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setName(self, name: TextHelper) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			name: the new name of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addEnchantment(self, id: str, level: int) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			level: the level of the enchantment 
			id: the id of the enchantment 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addEnchantment(self, enchantment: EnchantmentHelper) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to add 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clearEnchantments(self) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def removeEnchantment(self, enchantment: EnchantmentHelper) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			enchantment: the enchantment to remove 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def removeEnchantment(self, id: str) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			id: the id of the enchantment to remove 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clearLore(self) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setLore(self, lore: List[object]) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			lore: the new lore 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addLore(self, lore: List[object]) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			lore: the lore to add 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setUnbreakable(self, unbreakable: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			unbreakable: whether the item should be unbreakable or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideEnchantments(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide the enchantments or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideModifiers(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide attributes and modifiers or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideUnbreakable(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide the unbreakable flag or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideCanDestroy(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide the blocks this item can destroy or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideCanPlace(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide the blocks this item can be placed on or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideAdditional(self, hide: bool) -> "CreativeItemStackHelper":
		"""These flags are for banner patterns, potion effects, book information and other special
flags.\n
		Since: 1.8.4 

		Args:
			hide: whether to hide additional flags or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hideDye(self, hide: bool) -> "CreativeItemStackHelper":
		"""
		Since: 1.8.4 

		Args:
			hide: whether to hide the color of colored leather armor or not 

		Returns:
			self for chaining. 
		"""
		pass

	pass


