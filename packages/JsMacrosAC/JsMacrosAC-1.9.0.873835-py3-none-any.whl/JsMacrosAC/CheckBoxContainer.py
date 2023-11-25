from typing import overload
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .IContainerParent import IContainerParent

java_util_function_Consumer_java_lang_Boolean_ = TypeVar("java_util_function_Consumer_java_lang_Boolean_")
Consumer = java_util_function_Consumer_java_lang_Boolean_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class CheckBoxContainer(MultiElementContainer):
	message: Text

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, defaultState: bool, message: Text, parent: IContainerParent, setState: Consumer) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


