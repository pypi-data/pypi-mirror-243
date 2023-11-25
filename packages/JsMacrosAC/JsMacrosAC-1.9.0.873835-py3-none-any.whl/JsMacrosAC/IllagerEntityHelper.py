from typing import overload
from typing import TypeVar
from typing import Generic
from .MobEntityHelper import MobEntityHelper

T = TypeVar("T")

class IllagerEntityHelper(Generic[T], MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isCelebrating(self) -> bool:
		pass

	@overload
	def getState(self) -> str:
		pass

	pass


