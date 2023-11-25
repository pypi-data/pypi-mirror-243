from typing import overload
from typing import List
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .IOverlayParent import IOverlayParent

java_util_function_Consumer_java_lang_Integer_ = TypeVar("java_util_function_Consumer_java_lang_Integer_")
Consumer = java_util_function_Consumer_java_lang_Integer_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ListContainer(MultiElementContainer):
	onSelect: Consumer

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, list: List[Text], parent: IOverlayParent, onSelect: Consumer) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def addItem(self, name: Text) -> None:
		pass

	@overload
	def setSelected(self, index: int) -> None:
		pass

	@overload
	def onScrollbar(self, page: float) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


