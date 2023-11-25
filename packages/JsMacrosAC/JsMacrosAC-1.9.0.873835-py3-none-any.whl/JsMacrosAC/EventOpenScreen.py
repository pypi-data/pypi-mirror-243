from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .IScreen import IScreen

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class EventOpenScreen(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	screen: IScreen
	screenName: str

	@overload
	def __init__(self, screen: Screen) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


