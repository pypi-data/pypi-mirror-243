from typing import overload
from typing import TypeVar

java_util_function_Consumer_java_lang_Double_ = TypeVar("java_util_function_Consumer_java_lang_Double_")
Consumer = java_util_function_Consumer_java_lang_Double_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_gui_widget_ClickableWidget = TypeVar("net_minecraft_client_gui_widget_ClickableWidget")
ClickableWidget = net_minecraft_client_gui_widget_ClickableWidget


class Scrollbar(ClickableWidget):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, color: int, borderColor: int, highlightColor: int, scrollPages: float, onChange: Consumer) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> "Scrollbar":
		pass

	@overload
	def setScrollPages(self, scrollPages: float) -> None:
		pass

	@overload
	def scrollToPercent(self, percent: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onChange(self) -> None:
		pass

	@overload
	def mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> bool:
		pass

	@overload
	def renderButton(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


