from typing import overload
from typing import TypeVar
from typing import Generic

T = TypeVar("T")

class MixinPacketHandler(Generic[T]):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	pass


