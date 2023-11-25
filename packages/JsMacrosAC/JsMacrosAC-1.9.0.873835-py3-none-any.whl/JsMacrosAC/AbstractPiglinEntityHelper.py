from typing import overload
from typing import TypeVar
from typing import Generic
from .MobEntityHelper import MobEntityHelper

T = TypeVar("T")

class AbstractPiglinEntityHelper(Generic[T], MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def canBeZombified(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin can be zombified in the current dimension, 'false' otherwise. 
		"""
		pass

	pass


