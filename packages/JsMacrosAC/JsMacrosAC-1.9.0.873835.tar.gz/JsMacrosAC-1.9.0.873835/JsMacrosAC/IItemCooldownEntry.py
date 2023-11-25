from typing import overload


class IItemCooldownEntry:

	@overload
	def jsmacros_getStartTick(self) -> int:
		pass

	@overload
	def jsmacros_getEndTick(self) -> int:
		pass

	pass


