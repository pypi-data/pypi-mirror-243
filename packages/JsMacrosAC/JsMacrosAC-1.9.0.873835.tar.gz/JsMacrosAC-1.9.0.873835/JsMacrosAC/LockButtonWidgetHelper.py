from typing import overload
from typing import TypeVar
from .ClickableWidgetHelper import ClickableWidgetHelper

net_minecraft_client_gui_widget_LockButtonWidget = TypeVar("net_minecraft_client_gui_widget_LockButtonWidget")
LockButtonWidget = net_minecraft_client_gui_widget_LockButtonWidget


class LockButtonWidgetHelper(ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: LockButtonWidget) -> None:
		pass

	@overload
	def __init__(self, btn: LockButtonWidget, zIndex: int) -> None:
		pass

	@overload
	def isLocked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the button is locked, 'false' otherwise. 
		"""
		pass

	@overload
	def setLocked(self, locked: bool) -> "LockButtonWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			locked: whether to lock the button or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


