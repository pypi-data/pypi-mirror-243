from typing import overload


class DocletEnumType:

	@overload
	def name(self) -> str:
		pass

	@overload
	def type(self) -> str:
		pass

	pass


