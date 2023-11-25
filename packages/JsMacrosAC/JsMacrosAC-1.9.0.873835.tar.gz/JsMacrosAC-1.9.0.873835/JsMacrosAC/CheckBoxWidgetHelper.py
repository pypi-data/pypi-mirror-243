from typing import overload
from .ClickableWidgetHelper import ClickableWidgetHelper
from .CheckBox import CheckBox


class CheckBoxWidgetHelper(ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: CheckBox) -> None:
		pass

	@overload
	def __init__(self, btn: CheckBox, zIndex: int) -> None:
		pass

	@overload
	def isChecked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this button is checked, 'false' otherwise. 
		"""
		pass

	@overload
	def toggle(self) -> "CheckBoxWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setChecked(self, checked: bool) -> "CheckBoxWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			checked: whether to check or uncheck this button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


