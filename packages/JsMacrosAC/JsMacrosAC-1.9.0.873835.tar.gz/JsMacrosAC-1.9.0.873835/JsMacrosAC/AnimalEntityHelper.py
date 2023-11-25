from typing import overload
from typing import TypeVar
from typing import Generic
from .MobEntityHelper import MobEntityHelper
from .ItemHelper import ItemHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")

class AnimalEntityHelper(Generic[T], MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isFood(self, item: ItemHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check 

		Returns:
			'true' if the item can be used to feed and breed this animal, 'false' otherwise. 
		"""
		pass

	@overload
	def isFood(self, item: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check 

		Returns:
			'true' if the item can be used to feed and breed this animal, 'false' otherwise. 
		"""
		pass

	@overload
	def canBreedWith(self, other: "AnimalEntityHelper") -> bool:
		"""
		Since: 1.8.4 

		Args:
			other: the other animal to check 

		Returns:
			'true' if this animal can be bred with the other animal, 'false' otherwise. 
		"""
		pass

	pass


