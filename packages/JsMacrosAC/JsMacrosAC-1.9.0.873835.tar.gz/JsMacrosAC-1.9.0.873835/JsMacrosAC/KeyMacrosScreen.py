from typing import overload
from typing import TypeVar
from .MacroScreen import MacroScreen

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class KeyMacrosScreen(MacroScreen):

	@overload
	def __init__(self, parent: Screen) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def keyReleased(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def mouseReleased(self, mouseX: float, mouseY: float, button: int) -> bool:
		pass

	pass


