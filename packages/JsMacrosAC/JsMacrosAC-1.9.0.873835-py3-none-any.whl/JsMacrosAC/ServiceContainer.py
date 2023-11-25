from typing import overload
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .ServiceScreen import ServiceScreen
from .ServiceTrigger import ServiceTrigger

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

java_io_File = TypeVar("java_io_File")
File = java_io_File

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ServiceContainer(MultiElementContainer):
	service: str

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: ServiceScreen, service: str) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def getEnabled(self) -> bool:
		pass

	@overload
	def getRunning(self) -> bool:
		pass

	@overload
	def getTrigger(self) -> ServiceTrigger:
		pass

	@overload
	def setFile(self, file: File) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


