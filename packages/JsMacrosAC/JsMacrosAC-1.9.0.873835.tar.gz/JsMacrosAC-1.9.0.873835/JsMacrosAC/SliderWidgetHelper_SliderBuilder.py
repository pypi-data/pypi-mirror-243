from typing import overload
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .SliderWidgetHelper import SliderWidgetHelper


class SliderWidgetHelper_SliderBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen) -> None:
		pass

	@overload
	def getSteps(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of steps of this slider. 
		"""
		pass

	@overload
	def steps(self, steps: int) -> "SliderWidgetHelper_SliderBuilder":
		"""
		Since: 1.8.4 

		Args:
			steps: the amount of steps for the slider. Must be greater or equal to 2 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the initial value of the slider. 
		"""
		pass

	@overload
	def initially(self, value: int) -> "SliderWidgetHelper_SliderBuilder":
		"""
		Since: 1.8.4 

		Args:
			value: the initial value of the slider. Must be between 0 and steps - 1 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAction(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the change listener of the slider. 
		"""
		pass

	@overload
	def action(self, action: MethodWrapper) -> "SliderWidgetHelper_SliderBuilder":
		"""

		Args:
			action: the change listener for the slider 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> SliderWidgetHelper:
		pass

	pass


