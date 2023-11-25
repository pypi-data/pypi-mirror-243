from typing import overload
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_screen_ingame_CartographyTableScreen = TypeVar("net_minecraft_client_gui_screen_ingame_CartographyTableScreen")
CartographyTableScreen = net_minecraft_client_gui_screen_ingame_CartographyTableScreen


class CartographyInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: CartographyTableScreen) -> None:
		pass

	@overload
	def getMapItem(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the map item. 
		"""
		pass

	@overload
	def getMaterial(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the paper item. 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the output item. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


