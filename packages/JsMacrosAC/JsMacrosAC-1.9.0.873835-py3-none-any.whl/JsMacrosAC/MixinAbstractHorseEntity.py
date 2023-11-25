from typing import overload


class MixinAbstractHorseEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeGetInventorySize(self) -> int:
		pass

	pass


