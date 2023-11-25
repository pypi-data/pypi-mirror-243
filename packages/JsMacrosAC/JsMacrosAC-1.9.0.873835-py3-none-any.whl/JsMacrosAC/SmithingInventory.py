from typing import overload
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_SmithingScreen = TypeVar("net_minecraft_client_gui_screen_ingame_SmithingScreen")
SmithingScreen = net_minecraft_client_gui_screen_ingame_SmithingScreen


class SmithingInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: SmithingScreen) -> None:
		pass

	@overload
	def getLeftInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the left input item. 
		"""
		pass

	@overload
	def getRightInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the right input item. 
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


