from typing import overload
from typing import List
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_BrewingStandScreen = TypeVar("net_minecraft_client_gui_screen_ingame_BrewingStandScreen")
BrewingStandScreen = net_minecraft_client_gui_screen_ingame_BrewingStandScreen


class BrewingStandInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: BrewingStandScreen) -> None:
		pass

	@overload
	def isBrewablePotion(self, potion: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			potion: the potion to check 

		Returns:
			'true' if the given potion is can be brewed, 'false' otherwise. 
		"""
		pass

	@overload
	def isValidIngredient(self, ingredient: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			ingredient: the item to check 

		Returns:
			'true' if the given item is a valid ingredient, 'false' otherwise. 
		"""
		pass

	@overload
	def isValidRecipe(self, potion: ItemStackHelper, ingredient: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			potion: the potion to check 
			ingredient: the ingredient to check 

		Returns:
			'true' if the given potion and ingredient can be brewed together, 'false' otherwise. 
		"""
		pass

	@overload
	def getFuelCount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the left fuel. 
		"""
		pass

	@overload
	def getMaxFuelUses(self) -> int:
		"""The maximum fuel count is a constant with the value 20.\n
		Since: 1.8.4 

		Returns:
			the maximum fuel. 
		"""
		pass

	@overload
	def canBrewCurrentInput(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the brewing stand can brew any of the held potions with the current
ingredient, 'false' otherwise. 
		"""
		pass

	@overload
	def getBrewTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the time the potions have been brewing. 
		"""
		pass

	@overload
	def getRemainingTicks(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining time the potions have to brew. 
		"""
		pass

	@overload
	def previewPotion(self, potion: ItemStackHelper, ingredient: ItemStackHelper) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			potion: the potion 
			ingredient: the ingredient 

		Returns:
			the resulting potion of the given potion and ingredient if it exists and the potion
itself otherwise. 
		"""
		pass

	@overload
	def previewPotions(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all resulting potions of the current input. 
		"""
		pass

	@overload
	def getIngredient(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the ingredient. 
		"""
		pass

	@overload
	def getFuel(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the fuel item. 
		"""
		pass

	@overload
	def getFirstPotion(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the first potion. 
		"""
		pass

	@overload
	def getSecondPotion(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the second potion. 
		"""
		pass

	@overload
	def getThirdPotion(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the third potion. 
		"""
		pass

	@overload
	def getPotions(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of the potions inside the brewing stand. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


