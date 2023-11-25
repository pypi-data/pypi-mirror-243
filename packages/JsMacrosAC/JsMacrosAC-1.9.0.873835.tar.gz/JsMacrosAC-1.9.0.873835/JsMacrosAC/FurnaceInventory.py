from typing import overload
from typing import TypeVar
from typing import Mapping
from .RecipeInventory import RecipeInventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_AbstractFurnaceScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_AbstractFurnaceScreen__")
AbstractFurnaceScreen = net_minecraft_client_gui_screen_ingame_AbstractFurnaceScreen__


class FurnaceInventory(RecipeInventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: AbstractFurnaceScreen) -> None:
		pass

	@overload
	def getInput(self, x: int, y: int) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the input, will always be 0 
			y: the y position of the input, will always be 0 

		Returns:
			the currently smelting item. 
		"""
		pass

	@overload
	def getSmeltedItem(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the currently smelting item. 
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
	def canUseAsFuel(self, stack: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			stack: the item to check 

		Returns:
			'true' if the item is a valid fuel, 'false' otherwise. 
		"""
		pass

	@overload
	def isSmeltable(self, stack: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			stack: the item to check 

		Returns:
			'true' if the item can be smelted, 'false' otherwise. 
		"""
		pass

	@overload
	def getFuelValues(self) -> Mapping[str, int]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all valid fuels and their burn times in ticks. 
		"""
		pass

	@overload
	def getSmeltingProgress(self) -> int:
		"""If the returned value equals FurnaceInventory#getTotalSmeltingTime() then the item is done smelting.\n
		Since: 1.8.4 

		Returns:
			the current Smelting progress in ticks. 
		"""
		pass

	@overload
	def getTotalSmeltingTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the total smelting time of a single input item in ticks. 
		"""
		pass

	@overload
	def getRemainingSmeltingTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining time of the smelting progress in ticks. 
		"""
		pass

	@overload
	def getRemainingFuelTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining fuel time in ticks. 
		"""
		pass

	@overload
	def getTotalFuelTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the total fuel time of the current fuel item in ticks. 
		"""
		pass

	@overload
	def isBurning(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the furnace is currently smelting an item, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


