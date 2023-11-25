from typing import overload
from typing import TypeVar
from typing import Generic

java_io_Serializable = TypeVar("java_io_Serializable")
Serializable = java_io_Serializable

E = TypeVar("E")
E = E

java_util_AbstractSet_E_ = TypeVar("java_util_AbstractSet_E_")
AbstractSet = java_util_AbstractSet_E_


class SynchronizedWeakHashSet(Serializable, Generic[E], AbstractSet):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def size(self) -> int:
		pass

	@overload
	def contains(self, o: object) -> bool:
		pass

	@overload
	def add(self, o: E) -> bool:
		pass

	@overload
	def remove(self, o: object) -> bool:
		pass

	@overload
	def clear(self) -> None:
		pass

	@overload
	def iterator(self) -> iter:
		pass

	pass


