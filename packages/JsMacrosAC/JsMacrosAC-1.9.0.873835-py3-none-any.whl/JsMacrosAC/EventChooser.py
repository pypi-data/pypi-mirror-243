from typing import overload
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent

java_util_function_Consumer_java_lang_String_ = TypeVar("java_util_function_Consumer_java_lang_String_")
Consumer = java_util_function_Consumer_java_lang_String_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class EventChooser(OverlayContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, selected: str, parent: IOverlayParent, setEvent: Consumer) -> None:
		pass

	@overload
	def selectEvent(self, event: str) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def addEvent(self, eventName: str) -> None:
		pass

	@overload
	def updateEventPos(self) -> None:
		pass

	@overload
	def onScrollbar(self, page: float) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


