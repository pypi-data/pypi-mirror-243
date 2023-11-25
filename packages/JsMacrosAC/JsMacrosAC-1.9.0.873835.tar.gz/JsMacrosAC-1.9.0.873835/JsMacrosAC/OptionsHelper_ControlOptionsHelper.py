from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .OptionsHelper import OptionsHelper

net_minecraft_client_option_KeyBinding = TypeVar("net_minecraft_client_option_KeyBinding")
KeyBinding = net_minecraft_client_option_KeyBinding


class OptionsHelper_ControlOptionsHelper:
	parent: OptionsHelper

	@overload
	def __init__(self, OptionsHelper: OptionsHelper) -> None:
		pass

	@overload
	def getParent(self) -> OptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			the parent options helper. 
		"""
		pass

	@overload
	def getMouseSensitivity(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current mouse sensitivity. 
		"""
		pass

	@overload
	def setMouseSensitivity(self, val: float) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new mouse sensitivity 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isMouseInverted(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the mouse direction should be inverted. 
		"""
		pass

	@overload
	def invertMouse(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to invert the mouse direction or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMouseWheelSensitivity(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current mouse wheel sensitivity. 
		"""
		pass

	@overload
	def setMouseWheelSensitivity(self, val: float) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new mouse wheel sensitivity 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isDiscreteScrollingEnabled(self) -> bool:
		"""This option was introduced due to a bug on some systems where the mouse wheel would
scroll too fast.\n
		Since: 1.8.4 

		Returns:
			'true' if discrete scrolling is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableDiscreteScrolling(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable discrete scrolling or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isTouchscreenEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if touchscreen mode is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableTouchscreen(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable touchscreen mode or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRawMouseInputEnabled(self) -> bool:
		"""Raw input is directly reading the mouse data, without any adjustments due to other
programs or the operating system.\n
		Since: 1.8.4 

		Returns:
			'true' if raw mouse input is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableRawMouseInput(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable raw mouse input or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isAutoJumpEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if auto jump is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableAutoJump(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable auto jump or not or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isSneakTogglingEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the toggle functionality for sneaking is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def toggleSneak(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable or disable the toggle functionality for sneaking 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isSprintTogglingEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the toggle functionality for sprinting is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def toggleSprint(self, val: bool) -> "OptionsHelper_ControlOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable or disable the toggle functionality for sprinting 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRawKeys(self) -> List[KeyBinding]:
		"""
		Since: 1.8.4 

		Returns:
			an array of all raw minecraft keybindings. 
		"""
		pass

	@overload
	def getCategories(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all keybinding categories. 
		"""
		pass

	@overload
	def getKeys(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all key names. 
		"""
		pass

	@overload
	def getKeyBinds(self) -> Mapping[str, str]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all keybindings and their bound key. 
		"""
		pass

	@overload
	def getKeyBindsByCategory(self, category: str) -> Mapping[str, str]:
		"""
		Since: 1.8.4 

		Args:
			category: the category to get keybindings from 

		Returns:
			a map of all keybindings and their bound key in the specified category. 
		"""
		pass

	@overload
	def getKeyBindsByCategory(self) -> Mapping[str, Mapping[str, str]]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all keybinding categories, containing a map of all keybindings in that
category and their bound key. 
		"""
		pass

	pass


