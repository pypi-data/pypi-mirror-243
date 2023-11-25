from typing import overload
from typing import List
from .IDraw2D import IDraw2D
from .ClickableWidgetHelper import ClickableWidgetHelper
from .TextFieldWidgetHelper import TextFieldWidgetHelper
from .MethodWrapper import MethodWrapper
from .CheckBoxWidgetHelper import CheckBoxWidgetHelper
from .SliderWidgetHelper import SliderWidgetHelper
from .LockButtonWidgetHelper import LockButtonWidgetHelper
from .CyclingButtonWidgetHelper import CyclingButtonWidgetHelper
from .ButtonWidgetHelper_ButtonBuilder import ButtonWidgetHelper_ButtonBuilder
from .CheckBoxWidgetHelper_CheckBoxBuilder import CheckBoxWidgetHelper_CheckBoxBuilder
from .CyclingButtonWidgetHelper_CyclicButtonBuilder import CyclingButtonWidgetHelper_CyclicButtonBuilder
from .LockButtonWidgetHelper_LockButtonBuilder import LockButtonWidgetHelper_LockButtonBuilder
from .SliderWidgetHelper_SliderBuilder import SliderWidgetHelper_SliderBuilder
from .TextFieldWidgetHelper_TextFieldBuilder import TextFieldWidgetHelper_TextFieldBuilder
from .ButtonWidgetHelper_TexturedButtonBuilder import ButtonWidgetHelper_TexturedButtonBuilder


class IScreen(IDraw2D):
	"""
	Since: 1.2.7 
	"""

	@overload
	def getScreenClassName(self) -> str:
		"""
		Since: 1.2.7 
		"""
		pass

	@overload
	def getTitleText(self) -> str:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def getButtonWidgets(self) -> List[ClickableWidgetHelper]:
		"""in '1.3.1' updated to work with all button widgets not just ones added by scripts.\n
		Since: 1.0.5 
		"""
		pass

	@overload
	def getTextFields(self) -> List[TextFieldWidgetHelper]:
		"""in '1.3.1' updated to work with all text fields not just ones added by scripts.\n
		Since: 1.0.5 
		"""
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, text: str, callback: MethodWrapper) -> ClickableWidgetHelper:
		"""
		Since: 1.0.5 

		Args:
			x: 
			width: 
			y: 
			callback: calls your method as a Consumer ClickableWidgetHelper 
			text: 
			height: 
		"""
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, callback: MethodWrapper) -> ClickableWidgetHelper:
		"""
		Since: 1.4.0 

		Args:
			x: 
			width: 
			y: 
			callback: calls your method as a Consumer ClickableWidgetHelper 
			text: 
			height: 
			zIndex: 
		"""
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, text: str, checked: bool, showMessage: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			showMessage: whether to show the message or not 
			x: the x position of the checkbox 
			width: the width of the checkbox 
			y: the y position of the checkbox 
			checked: whether the checkbox is checked or not 
			callback: calls your method as a Consumer CheckBoxWidgetHelper 
			text: the text to display next to the checkbox 
			height: the height of the checkbox 

		Returns:
			a CheckBoxWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, text: str, checked: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the checkbox 
			width: the width of the checkbox 
			y: the y position of the checkbox 
			checked: whether the checkbox is checked or not 
			callback: calls your method as a Consumer CheckBoxWidgetHelper 
			text: the text to display next to the checkbox 
			height: the height of the checkbox 

		Returns:
			a CheckBoxWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, checked: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the checkbox 
			width: the width of the checkbox 
			y: the y position of the checkbox 
			checked: whether the checkbox is checked or not 
			callback: calls your method as a Consumer CheckBoxWidgetHelper 
			text: the text to display next to the checkbox 
			height: the height of the checkbox 
			zIndex: the z-index of the checkbox 

		Returns:
			a CheckBoxWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, checked: bool, showMessage: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			showMessage: whether to show the message or not 
			x: the x position of the checkbox 
			width: the width of the checkbox 
			y: the y position of the checkbox 
			checked: whether the checkbox is checked or not 
			callback: calls your method as a Consumer CheckBoxWidgetHelper 
			text: the text to display next to the checkbox 
			height: the height of the checkbox 
			zIndex: the z-index of the checkbox 

		Returns:
			a CheckBoxWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, text: str, value: float, steps: int, callback: MethodWrapper) -> SliderWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the slider 
			width: the width of the slider 
			y: the y position of the slider 
			callback: calls your method as a Consumer SliderWidgetHelper 
			text: the text to be displayed inside the slider 
			value: the initial value of the slider 
			steps: the number of steps the slider should have 
			height: the height of the slider 

		Returns:
			a SliderWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, value: float, steps: int, callback: MethodWrapper) -> SliderWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the slider 
			width: the width of the slider 
			y: the y position of the slider 
			callback: calls your method as a Consumer SliderWidgetHelper 
			text: the text to be displayed inside the slider 
			value: the initial value of the slider 
			steps: the number of steps the slider should have 
			height: the height of the slider 
			zIndex: the z-index of the slider 

		Returns:
			a SliderWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, text: str, value: float, callback: MethodWrapper) -> SliderWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the slider 
			width: the width of the slider 
			y: the y position of the slider 
			callback: calls your method as a Consumer SliderWidgetHelper 
			text: the text to be displayed inside the slider 
			value: the initial value of the slider 
			height: the height of the slider 

		Returns:
			a SliderWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, value: float, callback: MethodWrapper) -> SliderWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the slider 
			width: the width of the slider 
			y: the y position of the slider 
			callback: calls your method as a Consumer SliderWidgetHelper 
			text: the text to be displayed inside the slider 
			value: the initial value of the slider 
			height: the height of the slider 
			zIndex: the z-index of the slider 

		Returns:
			a SliderWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addLockButton(self, x: int, y: int, callback: MethodWrapper) -> LockButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the lock button 
			y: the y position of the lock button 
			callback: calls your method as a Consumer LockButtonWidgetHelper 

		Returns:
			LockButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addLockButton(self, x: int, y: int, zIndex: int, callback: MethodWrapper) -> LockButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the lock button 
			y: the y position of the lock button 
			callback: calls your method as a Consumer LockButtonWidgetHelper 
			zIndex: the z-index of the lock button 

		Returns:
			LockButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, values: List[str], initial: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			initial: the initial value of the cycling button 
			values: the values to cycle through 
			x: the x position of the cycling button 
			width: the width of the cycling button 
			y: the y position of the cycling button 
			callback: calls your method as a Consumer CyclingButtonWidgetHelper 
			height: the height of the cycling button 

		Returns:
			CyclingButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], initial: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			initial: the initial value of the cycling button 
			values: the values to cycle through 
			x: the x position of the cycling button 
			width: the width of the cycling button 
			y: the y position of the cycling button 
			callback: calls your method as a Consumer CyclingButtonWidgetHelper 
			height: the height of the cycling button 
			zIndex: the z-index of the cycling button 

		Returns:
			CyclingButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], alternatives: List[str], initial: str, prefix: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			initial: the initial value of the cycling button 
			prefix: the prefix of the values 
			values: the values to cycle through 
			x: the x position of the cycling button 
			width: the width of the cycling button 
			y: the y position of the cycling button 
			callback: calls your method as a Consumer CyclingButtonWidgetHelper 
			alternatives: the alternative values to cycle through 
			height: the height of the cycling button 
			zIndex: the z-index of the cycling button 

		Returns:
			CyclingButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], alternatives: List[str], initial: str, prefix: str, alternateToggle: MethodWrapper, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		"""
		Since: 1.8.4 

		Args:
			alternateToggle: the method to determine if the cycling button should use the
                       alternative values 
			initial: the initial value of the cycling button 
			prefix: the prefix of the values 
			values: the values to cycle through 
			x: the x position of the cycling button 
			width: the width of the cycling button 
			y: the y position of the cycling button 
			callback: calls your method as a Consumer CyclingButtonWidgetHelper 
			alternatives: the alternative values to cycle through 
			height: the height of the cycling button 
			zIndex: the z-index of the cycling button 

		Returns:
			CyclingButtonWidgetHelper for the given input. 
		"""
		pass

	@overload
	def removeButton(self, btn: ClickableWidgetHelper) -> "IScreen":
		"""
		Since: 1.0.5 

		Args:
			btn: 
		"""
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		"""
		Since: 1.0.5 

		Args:
			onChange: calls your method as a Consumer String 
			x: 
			width: 
			y: 
			message: 
			height: 
		"""
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, zIndex: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		"""
		Since: 1.0.5 

		Args:
			onChange: calls your method as a Consumer String 
			x: 
			width: 
			y: 
			message: 
			height: 
			zIndex: 
		"""
		pass

	@overload
	def removeTextInput(self, inp: TextFieldWidgetHelper) -> "IScreen":
		"""
		Since: 1.0.5 

		Args:
			inp: 
		"""
		pass

	@overload
	def setOnMouseDown(self, onMouseDown: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onMouseDown: calls your method as a BiConsumer Pos2D , Integer 
		"""
		pass

	@overload
	def setOnMouseDrag(self, onMouseDrag: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onMouseDrag: calls your method as a BiConsumer Vec2D , Integer 
		"""
		pass

	@overload
	def setOnMouseUp(self, onMouseUp: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onMouseUp: calls your method as a BiConsumer Pos2D , Integer 
		"""
		pass

	@overload
	def setOnScroll(self, onScroll: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onScroll: calls your method as a BiConsumer Pos2D , Double 
		"""
		pass

	@overload
	def setOnKeyPressed(self, onKeyPressed: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onKeyPressed: calls your method as a BiConsumer Integer , Integer 
		"""
		pass

	@overload
	def setOnCharTyped(self, onCharTyped: MethodWrapper) -> "IScreen":
		"""
		Since: 1.8.4 

		Args:
			onCharTyped: calls your method as a BiConsumer Character , Integer 
		"""
		pass

	@overload
	def setOnClose(self, onClose: MethodWrapper) -> "IScreen":
		"""
		Since: 1.2.7 

		Args:
			onClose: calls your method as a Consumer IScreen 
		"""
		pass

	@overload
	def close(self) -> None:
		"""
		Since: 1.1.9 
		"""
		pass

	@overload
	def reloadScreen(self) -> "IScreen":
		"""calls the screen's init function re-loading it.\n
		Since: 1.2.7 
		"""
		pass

	@overload
	def buttonBuilder(self) -> ButtonWidgetHelper_ButtonBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for buttons. 
		"""
		pass

	@overload
	def checkBoxBuilder(self) -> CheckBoxWidgetHelper_CheckBoxBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for checkboxes. 
		"""
		pass

	@overload
	def checkBoxBuilder(self, checked: bool) -> CheckBoxWidgetHelper_CheckBoxBuilder:
		"""
		Since: 1.8.4 

		Args:
			checked: whether the checkbox should be checked by default 

		Returns:
			a new builder for checkboxes. 
		"""
		pass

	@overload
	def cyclicButtonBuilder(self, valueToText: MethodWrapper) -> CyclingButtonWidgetHelper_CyclicButtonBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for cycling buttons. 
		"""
		pass

	@overload
	def lockButtonBuilder(self) -> LockButtonWidgetHelper_LockButtonBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for lock buttons. 
		"""
		pass

	@overload
	def lockButtonBuilder(self, locked: bool) -> LockButtonWidgetHelper_LockButtonBuilder:
		"""
		Since: 1.8.4 

		Args:
			locked: whether the lock button should be locked by default 

		Returns:
			a new builder for lock buttons. 
		"""
		pass

	@overload
	def sliderBuilder(self) -> SliderWidgetHelper_SliderBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for sliders. 
		"""
		pass

	@overload
	def textFieldBuilder(self) -> TextFieldWidgetHelper_TextFieldBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for text fields. 
		"""
		pass

	@overload
	def texturedButtonBuilder(self) -> ButtonWidgetHelper_TexturedButtonBuilder:
		"""
		Since: 1.8.4 

		Returns:
			a new builder for textured buttons. 
		"""
		pass

	@overload
	def isShiftDown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the shift key is pressed, 'false' otherwise. 
		"""
		pass

	@overload
	def isCtrlDown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the ctrl key is pressed, 'false' otherwise. 
		"""
		pass

	@overload
	def isAltDown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the alt key is pressed, 'false' otherwise. 
		"""
		pass

	@overload
	def getOnClose(self) -> MethodWrapper:
		pass

	pass


