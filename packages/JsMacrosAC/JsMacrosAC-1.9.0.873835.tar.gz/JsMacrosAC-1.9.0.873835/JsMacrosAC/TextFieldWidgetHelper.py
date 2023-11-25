from typing import overload
from typing import TypeVar
from .ClickableWidgetHelper import ClickableWidgetHelper
from .MethodWrapper import MethodWrapper

net_minecraft_client_gui_widget_TextFieldWidget = TypeVar("net_minecraft_client_gui_widget_TextFieldWidget")
TextFieldWidget = net_minecraft_client_gui_widget_TextFieldWidget


class TextFieldWidgetHelper(ClickableWidgetHelper):
	"""
	Since: 1.0.5 
	"""

	@overload
	def __init__(self, t: TextFieldWidget) -> None:
		pass

	@overload
	def __init__(self, t: TextFieldWidget, zIndex: int) -> None:
		pass

	@overload
	def getText(self) -> str:
		"""
		Since: 1.0.5 

		Returns:
			the currently entered String . 
		"""
		pass

	@overload
	def setText(self, text: str) -> "TextFieldWidgetHelper":
		"""
		Since: 1.0.5 

		Args:
			text: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setText(self, text: str, await_: bool) -> "TextFieldWidgetHelper":
		"""set the currently entered String .\n
		Since: 1.3.1 

		Args:
			await: 
			text: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setEditableColor(self, color: int) -> "TextFieldWidgetHelper":
		"""
		Since: 1.0.5 

		Args:
			color: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setEditable(self, edit: bool) -> "TextFieldWidgetHelper":
		"""
		Since: 1.0.5 

		Args:
			edit: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isEditable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the text field is editable, 'false' otherwise. 
		"""
		pass

	@overload
	def setUneditableColor(self, color: int) -> "TextFieldWidgetHelper":
		"""
		Since: 1.0.5 

		Args:
			color: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSelectedText(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the selected text. 
		"""
		pass

	@overload
	def setSuggestion(self, suggestion: str) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			suggestion: the suggestion to set 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMaxLength(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum length of this text field. 
		"""
		pass

	@overload
	def setMaxLength(self, length: int) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			length: the new maximum length 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setSelection(self, start: int, end: int) -> "TextFieldWidgetHelper":
		pass

	@overload
	def setTextPredicate(self, predicate: MethodWrapper) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			predicate: the text filter 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def resetTextPredicate(self) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorPosition(self, position: int) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			position: the cursor position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorPosition(self, position: int, shift: bool) -> "TextFieldWidgetHelper":
		"""
		Since: 1.9.0 

		Returns:
			the cursor position. 
		"""
		pass

	@overload
	def setCursorToStart(self) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorToStart(self, shift: bool) -> "TextFieldWidgetHelper":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorToEnd(self) -> "TextFieldWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorToEnd(self, shift: bool) -> "TextFieldWidgetHelper":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


