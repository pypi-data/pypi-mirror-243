from typing import overload
from .ClickableWidgetHelper import ClickableWidgetHelper
from .Slider import Slider


class SliderWidgetHelper(ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: Slider) -> None:
		pass

	@overload
	def __init__(self, btn: Slider, zIndex: int) -> None:
		pass

	@overload
	def getValue(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current value of this slider. 
		"""
		pass

	@overload
	def setValue(self, value: float) -> "SliderWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the new value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSteps(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the set amount of steps of this slider. 
		"""
		pass

	@overload
	def setSteps(self, steps: int) -> "SliderWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			steps: the amount of steps 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


