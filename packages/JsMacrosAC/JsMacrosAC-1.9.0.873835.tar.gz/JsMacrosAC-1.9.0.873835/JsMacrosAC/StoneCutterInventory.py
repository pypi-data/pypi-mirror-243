from typing import overload
from typing import List
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_StonecutterScreen = TypeVar("net_minecraft_client_gui_screen_ingame_StonecutterScreen")
StonecutterScreen = net_minecraft_client_gui_screen_ingame_StonecutterScreen


class StoneCutterInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: StonecutterScreen) -> None:
		pass

	@overload
	def getSelectedRecipeIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the selected recipe index. 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the output item for the selected recipe. 
		"""
		pass

	@overload
	def selectRecipe(self, idx: int) -> "StoneCutterInventory":
		"""
		Since: 1.8.4 

		Args:
			idx: the index to select 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAvailableRecipeCount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of available recipes. 
		"""
		pass

	@overload
	def getRecipes(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all available recipe results in the form of item stacks. 
		"""
		pass

	@overload
	def canCraft(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if there is a selected recipe, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


