from typing import overload


class MixinTextFieldWidget:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getEditable(self) -> bool:
		pass

	@overload
	def getMaxLength(self) -> int:
		pass

	pass


