from typing import overload
from .OptionsHelper import OptionsHelper


class OptionsHelper_AccessibilityOptionsHelper:
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
	def getNarratorMode(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current narrator mode. 
		"""
		pass

	@overload
	def setNarratorMode(self, mode: str) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the mode to set the narrator to. Must be either "OFF", "ALL", "CHAT", or
            "SYSTEM" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def areSubtitlesShown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if subtitles are enabled. 
		"""
		pass

	@overload
	def showSubtitles(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to show subtitles or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setTextBackgroundOpacity(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new opacity for the text background 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextBackgroundOpacity(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the opacity of the text background. 
		"""
		pass

	@overload
	def isBackgroundForChatOnly(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def enableBackgroundForChatOnly(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatOpacity(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current chat opacity. 
		"""
		pass

	@overload
	def setChatOpacity(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat opacity 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatLineSpacing(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current chat line spacing. 
		"""
		pass

	@overload
	def setChatLineSpacing(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat line spacing 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatDelay(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current chat delay in seconds. 
		"""
		pass

	@overload
	def setChatDelay(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat delay in seconds 

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
	def enableAutoJump(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
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
	def toggleSneak(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
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
	def toggleSprint(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable or disable the toggle functionality for sprinting 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getDistortionEffect(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current distortion effect scale. 
		"""
		pass

	@overload
	def setDistortionEffect(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new distortion effect scale 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getFovEffect(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current fov effect scale. 
		"""
		pass

	@overload
	def setFovEffect(self, val: float) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new fov effect scale 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isMonochromeLogoEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the monochrome logo is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableMonochromeLogo(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable the monochrome logo or not 

		Returns:
			the current helper instance for chaining. 
		"""
		pass

	@overload
	def areLightningFlashesHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if lighting flashes are hidden, 'false' otherwise. 
		"""
		pass

	@overload
	def setFovEffect(self, val: bool) -> "OptionsHelper_AccessibilityOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new fov value 

		Returns:
			self for chaining. 
		"""
		pass

	pass


