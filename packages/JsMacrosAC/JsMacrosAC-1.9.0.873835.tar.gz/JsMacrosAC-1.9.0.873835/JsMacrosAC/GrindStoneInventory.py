from typing import overload
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_GrindstoneScreen = TypeVar("net_minecraft_client_gui_screen_ingame_GrindstoneScreen")
GrindstoneScreen = net_minecraft_client_gui_screen_ingame_GrindstoneScreen


class GrindStoneInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: GrindstoneScreen) -> None:
		pass

	@overload
	def getTopInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the upper item to disenchant. 
		"""
		pass

	@overload
	def getBottomInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the bottom item to disenchant. 
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
	def simulateXp(self) -> int:
		"""Returns the minimum amount of xp dropped when disenchanting the input items. To calculate the
maximum amount of xp, just multiply the return value by 2.\n
		Since: 1.8.4 

		Returns:
			the minimum amount of xp the grindstone should return. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


