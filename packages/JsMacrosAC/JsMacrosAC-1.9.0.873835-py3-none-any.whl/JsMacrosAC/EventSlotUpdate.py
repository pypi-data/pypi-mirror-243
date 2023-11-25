from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ItemStackHelper import ItemStackHelper
from .Inventory import Inventory

net_minecraft_client_gui_screen_ingame_HandledScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_HandledScreen__")
HandledScreen = net_minecraft_client_gui_screen_ingame_HandledScreen__

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class EventSlotUpdate(BaseEvent):
	"""
	Since: 1.9.0 
	"""
	type: str
	slot: int
	oldStack: ItemStackHelper
	newStack: ItemStackHelper

	@overload
	def __init__(self, screen: HandledScreen, type: str, slot: int, oldStack: ItemStack, newStack: ItemStack) -> None:
		pass

	@overload
	def getInventory(self) -> Inventory:
		"""

		Returns:
			inventory associated with the event 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


