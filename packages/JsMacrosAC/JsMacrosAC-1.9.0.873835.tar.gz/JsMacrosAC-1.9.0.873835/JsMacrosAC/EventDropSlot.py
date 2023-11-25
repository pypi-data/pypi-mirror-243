from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .Inventory import Inventory

net_minecraft_client_gui_screen_ingame_HandledScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_HandledScreen__")
HandledScreen = net_minecraft_client_gui_screen_ingame_HandledScreen__


class EventDropSlot(BaseEvent):
	"""event triggered when an item is dropped\n
	Since: 1.6.4 
	"""
	slot: int
	all: bool

	@overload
	def __init__(self, screen: HandledScreen, slot: int, all: bool) -> None:
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


