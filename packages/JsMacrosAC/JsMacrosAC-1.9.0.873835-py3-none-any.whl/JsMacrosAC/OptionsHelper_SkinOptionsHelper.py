from typing import overload
from .OptionsHelper import OptionsHelper


class OptionsHelper_SkinOptionsHelper:
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
	def isCapeActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's cape should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isJacketActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's jacket should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isLeftSleeveActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's left sleeve should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isRightSleeveActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's right sleeve should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isLeftPantsActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's left pants should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isRightPantsActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's right pants should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isHatActivated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's hat should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def isRightHanded(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's main hand is the right one, 'false' otherwise. 
		"""
		pass

	@overload
	def isLeftHanded(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player's main hand is the left one, 'false' otherwise. 
		"""
		pass

	@overload
	def toggleCape(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the cape should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleJacket(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the jacket should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleLeftSleeve(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the left sleeve should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleRightSleeve(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the right sleeve should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleLeftPants(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the left pants should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleRightPants(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the right pants should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleHat(self, val: bool) -> "OptionsHelper_SkinOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether the hat should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toggleMainHand(self, hand: str) -> "OptionsHelper_SkinOptionsHelper":
		"""The hand must be either '"left"' or '"right"' .\n
		Since: 1.8.4 

		Args:
			hand: the hand to set as main hand 

		Returns:
			self for chaining. 
		"""
		pass

	pass


