from typing import overload
from typing import TypeVar
from typing import Generic
from .AnimalEntityHelper import AnimalEntityHelper
from .LivingEntityHelper import LivingEntityHelper

T = TypeVar("T")

class TameableEntityHelper(Generic[T], AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isTamed(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is tamed, 'false' otherwise. 
		"""
		pass

	@overload
	def isSitting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is sitting, 'false' otherwise. 
		"""
		pass

	@overload
	def getOwner(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the owner's uuid, or 'null' if the entity is not tamed. 
		"""
		pass

	@overload
	def isOwner(self, owner: LivingEntityHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			owner: the possible owner 

		Returns:
			'true' if the entity is tamed by the given owner, 'false' otherwise. 
		"""
		pass

	pass


