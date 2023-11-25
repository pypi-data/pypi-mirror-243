from typing import overload


class Event:

	@overload
	def value(self) -> str:
		pass

	@overload
	def oldName(self) -> str:
		pass

	@overload
	def cancellable(self) -> bool:
		pass

	@overload
	def joinable(self) -> bool:
		pass

	pass


