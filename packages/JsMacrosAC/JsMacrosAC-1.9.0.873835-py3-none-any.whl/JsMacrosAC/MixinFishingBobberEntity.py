from typing import overload


class MixinFishingBobberEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getCaughtFish(self) -> bool:
		pass

	pass


