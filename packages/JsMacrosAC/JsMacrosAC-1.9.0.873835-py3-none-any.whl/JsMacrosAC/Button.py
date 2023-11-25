from typing import overload
from typing import TypeVar

java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Button_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Button_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Button_

net_minecraft_client_gui_widget_PressableWidget = TypeVar("net_minecraft_client_gui_widget_PressableWidget")
PressableWidget = net_minecraft_client_gui_widget_PressableWidget

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class Button(PressableWidget):
	horizCenter: bool
	onPress: Consumer
	hovering: bool
	forceHover: bool

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, color: int, borderColor: int, highlightColor: int, textColor: int, message: Text, onPress: Consumer) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> "Button":
		pass

	@overload
	def cantRenderAllText(self) -> bool:
		pass

	@overload
	def setMessage(self, message: Text) -> None:
		pass

	@overload
	def setColor(self, color: int) -> None:
		pass

	@overload
	def setHighlightColor(self, color: int) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onRelease(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onPress(self) -> None:
		pass

	pass


