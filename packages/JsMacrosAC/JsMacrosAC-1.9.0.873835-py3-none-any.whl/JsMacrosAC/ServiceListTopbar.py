from typing import overload
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .ServiceScreen import ServiceScreen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ServiceListTopbar(MultiElementContainer):

	@overload
	def __init__(self, parent: ServiceScreen, x: int, y: int, width: int, height: int, textRenderer: TextRenderer) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


