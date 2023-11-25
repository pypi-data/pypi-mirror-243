from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .Inventory import Inventory
from .IScreen import IScreen

net_minecraft_client_gui_screen_ingame_HandledScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_HandledScreen__")
HandledScreen = net_minecraft_client_gui_screen_ingame_HandledScreen__


class EventContainerUpdate(BaseEvent):
	inventory: Inventory
	screen: IScreen

	@overload
	def __init__(self, screen: HandledScreen) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


