from typing import overload
from typing import TypeVar
from .BaseScreen import BaseScreen
from .BaseScriptContext import BaseScriptContext
from .RunningContextContainer import RunningContextContainer

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class CancelScreen(BaseScreen):

	@overload
	def __init__(self, parent: Screen) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def addContainer(self, t: BaseScriptContext) -> None:
		pass

	@overload
	def removeContainer(self, t: RunningContextContainer) -> None:
		pass

	@overload
	def updatePos(self) -> None:
		pass

	@overload
	def mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> bool:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def removed(self) -> None:
		pass

	@overload
	def close(self) -> None:
		pass

	pass


