from typing import overload
from .RecipeInventory import RecipeInventory
from .ItemStackHelper import ItemStackHelper


class CraftingInventory(RecipeInventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def getInput(self, x: int, y: int) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the input from 0 to 2, going left to right 
			y: the y position of the input from 0 to 2, going top to bottom 

		Returns:
			the input item at the given position. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


