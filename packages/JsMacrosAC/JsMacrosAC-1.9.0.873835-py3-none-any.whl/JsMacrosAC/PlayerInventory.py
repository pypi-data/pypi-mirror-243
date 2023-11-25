from typing import overload
from .RecipeInventory import RecipeInventory
from .ItemStackHelper import ItemStackHelper


class PlayerInventory(RecipeInventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def getInput(self, x: int, y: int) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the input from 0 to 1, going left to right 
			y: the y position of the input from 0 to 1, going top to bottom 

		Returns:
			the input item at the given position of the crafting grid. 
		"""
		pass

	@overload
	def isInHotbar(self, slot: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			slot: the slot to check 

		Returns:
			'true' if the slot is in the hotbar or the offhand slot, 'false' otherwise. 
		"""
		pass

	@overload
	def getOffhand(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item in the offhand. 
		"""
		pass

	@overload
	def getHelmet(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped helmet item. 
		"""
		pass

	@overload
	def getChestplate(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped chestplate item. 
		"""
		pass

	@overload
	def getLeggings(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped leggings item. 
		"""
		pass

	@overload
	def getBoots(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped boots item. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


