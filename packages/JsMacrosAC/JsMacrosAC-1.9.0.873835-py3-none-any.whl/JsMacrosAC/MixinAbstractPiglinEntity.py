from typing import overload


class MixinAbstractPiglinEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeIsImmuneToZombification(self) -> bool:
		pass

	pass


