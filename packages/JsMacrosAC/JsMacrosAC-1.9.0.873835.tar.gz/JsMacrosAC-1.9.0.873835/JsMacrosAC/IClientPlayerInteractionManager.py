from typing import overload


class IClientPlayerInteractionManager:

	@overload
	def jsmacros_getBlockBreakingCooldown(self) -> int:
		pass

	pass


