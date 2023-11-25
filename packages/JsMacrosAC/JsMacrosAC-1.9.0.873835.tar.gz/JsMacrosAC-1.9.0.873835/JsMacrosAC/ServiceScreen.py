from typing import overload
from typing import TypeVar
from .MacroScreen import MacroScreen
from .MultiElementContainer import MultiElementContainer

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class ServiceScreen(MacroScreen):

	@overload
	def __init__(self, parent: Screen) -> None:
		pass

	@overload
	def addService(self, service: str) -> None:
		pass

	@overload
	def removeMacro(self, macro: MultiElementContainer) -> None:
		pass

	@overload
	def setFile(self, macro: MultiElementContainer) -> None:
		pass

	@overload
	def close(self) -> None:
		pass

	pass


