from typing import overload
from typing import TypeVar
from .MacroScreen import MacroScreen

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class EventMacrosScreen(MacroScreen):

	@overload
	def __init__(self, parent: Screen) -> None:
		pass

	pass


