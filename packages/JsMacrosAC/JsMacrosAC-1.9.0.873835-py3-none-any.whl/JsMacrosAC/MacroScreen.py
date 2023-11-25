from typing import overload
from typing import TypeVar
from .BaseScreen import BaseScreen
from .ScriptTrigger import ScriptTrigger
from .MultiElementContainer import MultiElementContainer
from .MacroContainer import MacroContainer

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

java_io_File = TypeVar("java_io_File")
File = java_io_File


class MacroScreen(BaseScreen):

	@overload
	def __init__(self, parent: Screen) -> None:
		pass

	@overload
	def mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> bool:
		pass

	@overload
	def addMacro(self, macro: ScriptTrigger) -> None:
		pass

	@overload
	def setFile(self, macro: MultiElementContainer) -> None:
		pass

	@overload
	def setEvent(self, macro: MacroContainer) -> None:
		pass

	@overload
	def runFile(self) -> None:
		pass

	@overload
	def confirmRemoveMacro(self, macro: MultiElementContainer) -> None:
		pass

	@overload
	def removeMacro(self, macro: MultiElementContainer) -> None:
		pass

	@overload
	def setMacroPos(self) -> None:
		pass

	@overload
	def editFile(self, file: File) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def updateSettings(self) -> None:
		pass

	@overload
	def removed(self) -> None:
		pass

	pass


