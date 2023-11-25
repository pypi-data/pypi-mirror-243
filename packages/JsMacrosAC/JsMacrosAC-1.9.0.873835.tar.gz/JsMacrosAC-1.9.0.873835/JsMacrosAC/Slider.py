from typing import overload
from typing import TypeVar

java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Slider_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Slider_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_Slider_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_gui_widget_ClickableWidget = TypeVar("net_minecraft_client_gui_widget_ClickableWidget")
ClickableWidget = net_minecraft_client_gui_widget_ClickableWidget

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class Slider(ClickableWidget):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, value: float, action: Consumer, steps: int) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, value: float, action: Consumer) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def roundValue(self, value: float) -> float:
		pass

	@overload
	def getValue(self) -> float:
		pass

	@overload
	def setValue(self, mouseX: float) -> None:
		pass

	@overload
	def getSteps(self) -> int:
		pass

	@overload
	def setSteps(self, steps: int) -> None:
		pass

	@overload
	def renderButton(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onRelease(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def setMessage(self, message: str) -> None:
		pass

	@overload
	def setMessage(self, message: Text) -> None:
		pass

	pass


