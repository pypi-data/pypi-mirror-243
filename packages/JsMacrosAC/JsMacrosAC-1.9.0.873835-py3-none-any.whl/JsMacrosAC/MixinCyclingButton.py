from typing import overload
from typing import TypeVar

java_util_function_Function_T,net_minecraft_text_Text_ = TypeVar("java_util_function_Function_T,net_minecraft_text_Text_")
Function = java_util_function_Function_T,net_minecraft_text_Text_

T = TypeVar("T")
net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class MixinCyclingButton:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeCycle(self, amount: int) -> None:
		pass

	@overload
	def invokeComposeText(self, value: T) -> Text:
		pass

	@overload
	def getValueToText(self) -> Function:
		pass

	pass


