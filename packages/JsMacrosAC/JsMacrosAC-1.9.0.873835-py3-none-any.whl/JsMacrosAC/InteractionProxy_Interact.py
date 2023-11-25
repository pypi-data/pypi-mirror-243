from typing import overload


class InteractionProxy_Interact:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def setOverride(self, value: bool) -> None:
		pass

	@overload
	def isInteracting(self) -> bool:
		pass

	@overload
	def ensureInteracting(self, cooldown: int) -> None:
		pass

	pass


