from typing import overload
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_AnvilScreen = TypeVar("net_minecraft_client_gui_screen_ingame_AnvilScreen")
AnvilScreen = net_minecraft_client_gui_screen_ingame_AnvilScreen


class AnvilInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: AnvilScreen) -> None:
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the currently set name to be applied. 
		"""
		pass

	@overload
	def setName(self, name: str) -> "AnvilInventory":
		"""The change will be applied once the item is taken out of the anvil.\n
		Since: 1.8.4 

		Args:
			name: the new item name 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getLevelCost(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the level cost to apply the changes. 
		"""
		pass

	@overload
	def getItemRepairCost(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of item needed to fully repair the item. 
		"""
		pass

	@overload
	def getMaximumLevelCost(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum default level cost. 
		"""
		pass

	@overload
	def getLeftInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the first input item. 
		"""
		pass

	@overload
	def getRightInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the second input item. 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the expected output item. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


