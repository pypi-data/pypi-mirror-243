from typing import overload


class TickSync_TickSyncInt(Comparable):
	tick: int

	@overload
	def __init__(self, tick: int) -> None:
		pass

	@overload
	def compareTo(self, o: "TickSync_TickSyncInt") -> int:
		pass

	pass


