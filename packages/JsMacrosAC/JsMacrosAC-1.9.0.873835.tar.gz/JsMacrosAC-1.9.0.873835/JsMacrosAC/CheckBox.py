from typing import overload
from typing import TypeVar

java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_CheckBox_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_CheckBox_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_wagyourgui_elements_CheckBox_

net_minecraft_client_gui_widget_CheckboxWidget = TypeVar("net_minecraft_client_gui_widget_CheckboxWidget")
CheckboxWidget = net_minecraft_client_gui_widget_CheckboxWidget

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class CheckBox(CheckboxWidget):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, checked: bool, action: Consumer) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, checked: bool, showMessage: bool, action: Consumer) -> None:
		pass

	@overload
	def onPress(self) -> None:
		pass

	pass


