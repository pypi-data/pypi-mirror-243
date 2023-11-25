from typing import overload
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .ButtonWidgetHelper import ButtonWidgetHelper


class ButtonWidgetHelper_ButtonBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen) -> None:
		pass

	@overload
	def height(self, height: int) -> "ButtonWidgetHelper_ButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			height: this argument is ignored and will always be set to 20 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> "ButtonWidgetHelper_ButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the button 
			height: this argument is ignored and will always be set to 20 

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
	def action(self, action: MethodWrapper) -> "ButtonWidgetHelper_ButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the action to run when the button is pressed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> ButtonWidgetHelper:
		pass

	pass


