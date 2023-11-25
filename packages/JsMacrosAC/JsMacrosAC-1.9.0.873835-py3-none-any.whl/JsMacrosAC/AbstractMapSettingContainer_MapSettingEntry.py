from typing import overload
from typing import TypeVar
from typing import Generic
from .MultiElementContainer import MultiElementContainer
from .AbstractMapSettingContainer import AbstractMapSettingContainer

T = TypeVar("T")
net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class AbstractMapSettingContainer_MapSettingEntry(Generic[T], MultiElementContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, textRenderer: TextRenderer, parent: AbstractMapSettingContainer, key: str, value: T) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def setKey(self, newKey: str) -> None:
		pass

	@overload
	def setValue(self, newValue: T) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


