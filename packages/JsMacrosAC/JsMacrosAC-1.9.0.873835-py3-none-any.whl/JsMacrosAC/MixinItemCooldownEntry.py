from typing import overload
from .IItemCooldownEntry import IItemCooldownEntry


class MixinItemCooldownEntry(IItemCooldownEntry):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getStartTick(self) -> int:
		pass

	@overload
	def jsmacros_getEndTick(self) -> int:
		pass

	pass


