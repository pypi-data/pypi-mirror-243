from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper
from .RecipeHelper import RecipeHelper

T = TypeVar("T")

class RecipeInventory(Generic[T], Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the output item. 
		"""
		pass

	@overload
	def getInputSize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum input size for all recipes in this inventory. 
		"""
		pass

	@overload
	def getInput(self, x: int, z: int) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the input slot, starting at 0, left to right. Must be less than RecipeInventory#getCraftingWidth() 
			z: the z position of the input slot, starting at 0, top to bottom. Must be less than RecipeInventory#getCraftingHeight() 

		Returns:
			the input item at the given position. 
		"""
		pass

	@overload
	def getInput(self) -> List[List[ItemStackHelper]]:
		"""
		Since: 1.8.4 

		Returns:
			the input items of the crafting grid, in a 2d array. 
		"""
		pass

	@overload
	def getCraftingWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the crafting grid. 
		"""
		pass

	@overload
	def getCraftingHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the crafting grid. 
		"""
		pass

	@overload
	def getCraftingSlotCount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of slots used for crafting. 
		"""
		pass

	@overload
	def getCategory(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the recipe category of recipes that can be crafted in this inventory. 
		"""
		pass

	@overload
	def getCraftableRecipes(self) -> List[RecipeHelper]:
		"""
		Since: 1.3.1 
		"""
		pass

	@overload
	def getRecipes(self, craftable: bool) -> List[RecipeHelper]:
		"""
		Since: 1.8.4 

		Args:
			craftable: whether only to list craftable recipes 

		Returns:
			a list of recipes that can be crafted in this inventory. 
		"""
		pass

	@overload
	def isRecipeBookOpened(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the recipe book is visible, 'false' otherwise. 
		"""
		pass

	@overload
	def toggleRecipeBook(self) -> None:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def setRecipeBook(self, open: bool) -> None:
		"""
		Since: 1.8.4 

		Args:
			open: whether to open or close the recipe book 
		"""
		pass

	pass


