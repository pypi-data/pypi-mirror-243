from typing import overload
from typing import TypeVar
from typing import Generic
from .Inventory import Inventory

T = TypeVar("T")

class ContainerInventory(Generic[T], Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: T) -> None:
		pass

	@overload
	def findFreeContainerSlot(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first free slot in this container. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


