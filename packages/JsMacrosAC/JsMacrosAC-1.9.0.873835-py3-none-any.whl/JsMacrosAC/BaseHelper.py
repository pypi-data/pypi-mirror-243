from typing import overload
from typing import TypeVar
from typing import Generic

T = TypeVar("T")

class BaseHelper(Generic[T]):

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def getRaw(self) -> T:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def equals(self, obj: object) -> bool:
		pass

	pass


