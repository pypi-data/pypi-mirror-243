from typing import overload
from typing import List
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent

java_util_function_Consumer_java_lang_Integer_ = TypeVar("java_util_function_Consumer_java_lang_Integer_")
Consumer = java_util_function_Consumer_java_lang_Integer_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class SelectorDropdownOverlay(OverlayContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, choices: List[Text], textRenderer: TextRenderer, parent: IOverlayParent, onChoice: Consumer) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def onScroll(self, page: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def setSelected(self, sel: int) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


