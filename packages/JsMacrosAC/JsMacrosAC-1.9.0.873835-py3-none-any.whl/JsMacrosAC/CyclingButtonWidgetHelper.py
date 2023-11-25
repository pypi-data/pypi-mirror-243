from typing import overload
from typing import TypeVar
from typing import Generic
from .ClickableWidgetHelper import ClickableWidgetHelper

T = TypeVar("T")
net_minecraft_client_gui_widget_CyclingButtonWidget_T_ = TypeVar("net_minecraft_client_gui_widget_CyclingButtonWidget_T_")
CyclingButtonWidget = net_minecraft_client_gui_widget_CyclingButtonWidget_T_


class CyclingButtonWidgetHelper(Generic[T], ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: CyclingButtonWidget) -> None:
		pass

	@overload
	def __init__(self, btn: CyclingButtonWidget, zIndex: int) -> None:
		pass

	@overload
	def getValue(self) -> T:
		"""
		Since: 1.8.4 

		Returns:
			the current value. 
		"""
		pass

	@overload
	def getStringValue(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current value in their string representation. 
		"""
		pass

	@overload
	def setValue(self, val: T) -> bool:
		"""
		Since: 1.8.4 

		Args:
			val: the new value 

		Returns:
			'true' if the value has changed, 'false' otherwise. 
		"""
		pass

	@overload
	def cycle(self, amount: int) -> "CyclingButtonWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			amount: the amount to cycle by 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def forward(self) -> "CyclingButtonWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def backward(self) -> "CyclingButtonWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


