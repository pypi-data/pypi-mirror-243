from typing import overload
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .CheckBoxWidgetHelper import CheckBoxWidgetHelper


class CheckBoxWidgetHelper_CheckBoxBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen) -> None:
		pass

	@overload
	def isChecked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the checkbox is initially checked, 'false' otherwise. 
		"""
		pass

	@overload
	def checked(self, checked: bool) -> "CheckBoxWidgetHelper_CheckBoxBuilder":
		"""
		Since: 1.8.4 

		Args:
			checked: whether the checkbox is initially checked or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAction(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the action to run when the button is pressed. 
		"""
		pass

	@overload
	def action(self, action: MethodWrapper) -> "CheckBoxWidgetHelper_CheckBoxBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the action to run when the button is pressed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> CheckBoxWidgetHelper:
		pass

	pass


