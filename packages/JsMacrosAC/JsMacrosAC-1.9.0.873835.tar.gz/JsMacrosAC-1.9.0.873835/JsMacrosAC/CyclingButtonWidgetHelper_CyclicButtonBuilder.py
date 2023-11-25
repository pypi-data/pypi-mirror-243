from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .TextHelper import TextHelper
from .CyclingButtonWidgetHelper import CyclingButtonWidgetHelper

T = TypeVar("T")

class CyclingButtonWidgetHelper_CyclicButtonBuilder(Generic[T], AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen, valueToText: MethodWrapper) -> None:
		pass

	@overload
	def getInitialValue(self) -> T:
		"""
		Since: 1.8.4 

		Returns:
			the initial value of the slider. 
		"""
		pass

	@overload
	def initially(self, value: T) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			value: the initial value of the slider 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getOption(self) -> TextHelper:
		"""The option text is a prefix of all values, separated by a colon.\n
		Since: 1.8.4 

		Returns:
			the option text of the button or an empty text if it is omitted. 
		"""
		pass

	@overload
	def option(self, option: str) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			option: the option text of the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def option(self, option: TextHelper) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			option: the option text of the button 

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
	def action(self, action: MethodWrapper) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the action to run when the button is pressed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getValueToText(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the function to convert a value to a text. 
		"""
		pass

	@overload
	def valueToText(self, valueToText: MethodWrapper) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			valueToText: the function to convert a value to a text 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getDefaultValues(self) -> List[T]:
		"""The button will normally cycle through the default values, but if the alternate toggle is
true, it will cycle through the alternate values.\n
		Since: 1.8.4 

		Returns:
			the list of all default values. 
		"""
		pass

	@overload
	def getAlternateValues(self) -> List[T]:
		"""The button will normally cycle through the default values, but if the alternate toggle is
true, it will cycle through the alternate values.\n
		Since: 1.8.4 

		Returns:
			the list of all alternate values. 
		"""
		pass

	@overload
	def values(self, values: List[T]) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			values: the default values of the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alternatives(self, values: List[T]) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			values: the alternate values of the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def values(self, defaults: List[T], alternatives: List[T]) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			defaults: the default values of the button 
			alternatives: the alternate values of the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def values(self, defaults: List[T], alternatives: List[T]) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			defaults: the default values of the button 
			alternatives: the alternate values of the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAlternateToggle(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the toggle function to determine if the button should cycle through the default
or the alternate values. 
		"""
		pass

	@overload
	def alternateToggle(self, alternateToggle: MethodWrapper) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			alternateToggle: the toggle function to determine if the button should cycle
                       through the default or the alternate values 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isOptionTextOmitted(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the prefix option text should be omitted, 'false' otherwise. 
		"""
		pass

	@overload
	def omitTextOption(self, optionTextOmitted: bool) -> "CyclingButtonWidgetHelper_CyclicButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			optionTextOmitted: whether the prefix option text should be omitted or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> CyclingButtonWidgetHelper:
		pass

	pass


