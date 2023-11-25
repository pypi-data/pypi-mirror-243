from typing import overload
from .OptionsHelper import OptionsHelper


class OptionsHelper_ChatOptionsHelper:
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
	def getChatVisibility(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current chat visibility mode. 
		"""
		pass

	@overload
	def setChatVisibility(self, mode: str) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the new chat visibility mode. Must be "FULL", "SYSTEM" or "HIDDEN 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def areColorsShown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if messages can use color codes, 'false' otherwise. 
		"""
		pass

	@overload
	def setShowColors(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to allow color codes in messages or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def areWebLinksEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if it's allowed to open web links from chat, 'false' otherwise. 
		"""
		pass

	@overload
	def enableWebLinks(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to allow opening web links from chat or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isWebLinkPromptEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if a warning prompt before opening links should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def enableWebLinkPrompt(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to show warning prompts before opening links or not 

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
	def setChatOpacity(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat opacity 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setTextBackgroundOpacity(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new background opacity for text 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextBackgroundOpacity(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current background opacity of text. 
		"""
		pass

	@overload
	def getTextSize(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current text size. 
		"""
		pass

	@overload
	def setTextSize(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new text size 

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
	def setChatLineSpacing(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
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
	def setChatDelay(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat delay in seconds 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatWidth(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current chat width. 
		"""
		pass

	@overload
	def setChatWidth(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new chat width 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatFocusedHeight(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the focused chat height. 
		"""
		pass

	@overload
	def setChatFocusedHeight(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new focused chat height 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChatUnfocusedHeight(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the unfocused chat height. 
		"""
		pass

	@overload
	def setChatUnfocusedHeight(self, val: float) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new unfocused chat height 

		Returns:
			self for chaining. 
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
	def setNarratorMode(self, mode: str) -> "OptionsHelper_ChatOptionsHelper":
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
	def areCommandSuggestionsEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if command suggestions are enabled 
		"""
		pass

	@overload
	def enableCommandSuggestions(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable command suggestions or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def areMatchedNamesHidden(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if messages from blocked users are hidden. 
		"""
		pass

	@overload
	def enableHideMatchedNames(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to hide messages of blocked users or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isDebugInfoReduced(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if reduced debug info is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def reduceDebugInfo(self, val: bool) -> "OptionsHelper_ChatOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable reduced debug info or not 

		Returns:
			self for chaining. 
		"""
		pass

	pass


