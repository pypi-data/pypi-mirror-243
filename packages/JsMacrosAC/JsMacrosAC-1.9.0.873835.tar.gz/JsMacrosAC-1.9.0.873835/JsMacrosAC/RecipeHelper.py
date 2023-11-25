from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .ItemStackHelper import ItemStackHelper

net_minecraft_recipe_RecipeEntry__ = TypeVar("net_minecraft_recipe_RecipeEntry__")
RecipeEntry = net_minecraft_recipe_RecipeEntry__


class RecipeHelper(BaseHelper):
	"""
	Since: 1.3.1 
	"""

	@overload
	def __init__(self, base: RecipeEntry, syncId: int) -> None:
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.3.1 
		"""
		pass

	@overload
	def getIngredients(self) -> List[List[ItemStackHelper]]:
		"""get ingredients list\n
		Since: 1.8.3 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.3.1 
		"""
		pass

	@overload
	def craft(self, craftAll: bool) -> "RecipeHelper":
		"""
		Since: 1.3.1 

		Args:
			craftAll: 
		"""
		pass

	@overload
	def getGroup(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the type of this recipe. 
		"""
		pass

	@overload
	def hasRecipeRemainders(self) -> bool:
		"""This will not account for the actual items used in the recipe, but only the default recipe
itself. Items with durability or with a lot of tags will probably not work correctly.\n
		Since: 1.8.4 

		Returns:
			will return 'true' if any of the default ingredients have a recipe remainder. 
		"""
		pass

	@overload
	def getRecipeRemainders(self) -> List[List[ItemStackHelper]]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all possible recipe remainders. 
		"""
		pass

	@overload
	def getType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the type of this recipe. 
		"""
		pass

	@overload
	def canCraft(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the recipe can be crafted with the current inventory, 'false' otherwise. 
		"""
		pass

	@overload
	def canCraft(self, amount: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			amount: the amount of items to craft 

		Returns:
			'true' if the given amount of items can be crafted with the current inventory, 'false' otherwise. 
		"""
		pass

	@overload
	def getCraftableAmount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			how often the recipe can be crafted with the current player inventory. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


