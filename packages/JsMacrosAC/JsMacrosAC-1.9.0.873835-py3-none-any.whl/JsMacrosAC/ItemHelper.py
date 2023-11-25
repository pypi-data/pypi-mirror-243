from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper
from .BlockHelper import BlockHelper
from .BlockStateHelper import BlockStateHelper
from .FoodComponentHelper import FoodComponentHelper

net_minecraft_item_Item = TypeVar("net_minecraft_item_Item")
Item = net_minecraft_item_Item


class ItemHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: Item) -> None:
		pass

	@overload
	def getCreativeTab(self) -> List[TextHelper]:
		"""
		Since: 1.8.4 

		Returns:
			the name of this item's group or '"UNKNOWN"' if this item is not in a group. 
		"""
		pass

	@overload
	def getGroupIcon(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			the item stack representing the group of this item or 'null' if this item is
not in a group. 
		"""
		pass

	@overload
	def canBeRepairedWith(self, stack: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			stack: the possible repair material 

		Returns:
			'true' if the given item stack can be used to repair item stacks of this item, 'false' otherwise. 
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
	def isBlockItem(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the item has a block representation, 'false' otherwise. 
		"""
		pass

	@overload
	def getBlock(self) -> BlockHelper:
		"""
		Since: 1.8.4 

		Returns:
			the block representation of this item or 'null' if this item has no
corresponding block. 
		"""
		pass

	@overload
	def getMiningSpeedMultiplier(self, state: BlockStateHelper) -> float:
		"""
		Since: 1.8.4 

		Args:
			state: the block state to check 

		Returns:
			the mining speed of this item against the given block state, returns '1' by
default. 
		"""
		pass

	@overload
	def isDamageable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the item has durability, 'false' otherwise. 
		"""
		pass

	@overload
	def hasRecipeRemainder(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if when crafter the item stack has a remainder, 'false' otherwise. 
		"""
		pass

	@overload
	def getRecipeRemainder(self) -> "ItemHelper":
		"""
		Since: 1.8.4 

		Returns:
			the recipe remainder if it exists and 'null' otherwise. 
		"""
		pass

	@overload
	def getEnchantability(self) -> int:
		"""With increased enchantability the change to get more and better enchantments increases.\n
		Since: 1.8.4 

		Returns:
			the enchantability of this item, returns '0' by default. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this item, translated to the current language. 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of this item. 
		"""
		pass

	@overload
	def getMaxCount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum amount of items in a stack of this item. 
		"""
		pass

	@overload
	def getMaxDurability(self) -> int:
		"""The damage an item has taken is the opposite of the durability still left.\n
		Since: 1.8.4 

		Returns:
			the maximum amount of damage this item can take. 
		"""
		pass

	@overload
	def isFireproof(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item is fireproof, 'false' otherwise. 
		"""
		pass

	@overload
	def isTool(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item is a tool, 'false' otherwise. 
		"""
		pass

	@overload
	def isWearable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item can be worn in the armor slot, 'false' otherwise. 
		"""
		pass

	@overload
	def isFood(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item is food, 'false' otherwise. 
		"""
		pass

	@overload
	def getFood(self) -> FoodComponentHelper:
		"""
		Since: 1.8.4 

		Returns:
			the food component of this item or 'null' if this item is not food. 
		"""
		pass

	@overload
	def canBeNested(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item can be nested, i.e. put into a bundle or shulker box, 'false' otherwise. 
		"""
		pass

	@overload
	def getDefaultStack(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the default item stack of this item with a stack size of '1' . 
		"""
		pass

	@overload
	def getStackWithNbt(self, nbt: str) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			nbt: the nbt data of the item stack 

		Returns:
			the item stack of this item with a stack size of '1' and the given nbt. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


