from typing import overload
from typing import TypeVar

net_minecraft_client_gui_widget_TextFieldWidget = TypeVar("net_minecraft_client_gui_widget_TextFieldWidget")
TextFieldWidget = net_minecraft_client_gui_widget_TextFieldWidget


class MixinAnvilScreen:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getNameField(self) -> TextFieldWidget:
		pass

	pass


