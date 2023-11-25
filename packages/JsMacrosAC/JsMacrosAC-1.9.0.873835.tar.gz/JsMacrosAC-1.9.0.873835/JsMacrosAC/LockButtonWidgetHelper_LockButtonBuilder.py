from typing import overload
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .LockButtonWidgetHelper import LockButtonWidgetHelper


class LockButtonWidgetHelper_LockButtonBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen) -> None:
		pass

	@overload
	def isLocked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			the initial state of the lock button. 
		"""
		pass

	@overload
	def locked(self, locked: bool) -> "LockButtonWidgetHelper_LockButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			locked: whether to initially lock the button or not 

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
	def action(self, action: MethodWrapper) -> "LockButtonWidgetHelper_LockButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the action to run when the button is pressed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> LockButtonWidgetHelper:
		pass

	pass


