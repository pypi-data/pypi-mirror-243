from typing import overload
from typing import TypeVar
from typing import Generic
from .AbstractHorseEntityHelper import AbstractHorseEntityHelper

T = TypeVar("T")

class DonkeyEntityHelper(Generic[T], AbstractHorseEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def hasChest(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the donkey is carrying a chest, 'false' otherwise. 
		"""
		pass

	pass


