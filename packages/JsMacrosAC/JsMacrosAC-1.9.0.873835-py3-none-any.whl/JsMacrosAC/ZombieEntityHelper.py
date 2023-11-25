from typing import overload
from typing import TypeVar
from typing import Generic
from .MobEntityHelper import MobEntityHelper

T = TypeVar("T")

class ZombieEntityHelper(Generic[T], MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isConvertingToDrowned(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this zombie is converting to a drowned, 'false' otherwise. 
		"""
		pass

	pass


