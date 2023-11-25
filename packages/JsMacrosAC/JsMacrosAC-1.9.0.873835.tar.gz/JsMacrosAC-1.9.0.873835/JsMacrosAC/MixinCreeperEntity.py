from typing import overload


class MixinCreeperEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getFuseTime(self) -> int:
		pass

	@overload
	def getMaxFuseTime(self) -> int:
		pass

	pass


