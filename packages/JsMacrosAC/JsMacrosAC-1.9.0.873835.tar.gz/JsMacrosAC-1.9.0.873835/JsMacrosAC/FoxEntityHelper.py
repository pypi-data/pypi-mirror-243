from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper
from .ItemStackHelper import ItemStackHelper
from .EntityHelper import EntityHelper

net_minecraft_entity_passive_FoxEntity = TypeVar("net_minecraft_entity_passive_FoxEntity")
FoxEntity = net_minecraft_entity_passive_FoxEntity


class FoxEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FoxEntity) -> None:
		pass

	@overload
	def getItemInMouth(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item in this fox's mouth. 
		"""
		pass

	@overload
	def isSnowFox(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is a snow fox, 'false' otherwise. 
		"""
		pass

	@overload
	def isRedFox(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is a red fox, 'false' otherwise. 
		"""
		pass

	@overload
	def getOwner(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the owner's UUID, or 'null' if this fox has no owner. 
		"""
		pass

	@overload
	def getSecondOwner(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the second owner's name, or 'null' if this fox has no owner. 
		"""
		pass

	@overload
	def canTrust(self, entity: EntityHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			entity: the entity to check 

		Returns:
			'true' if this fox trusts the given entity, 'false' otherwise. 
		"""
		pass

	@overload
	def hasFoundTarget(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is preparing its jump, 'false' otherwise. 
		"""
		pass

	@overload
	def isSitting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is sitting, 'false' otherwise. 
		"""
		pass

	@overload
	def isWandering(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is wandering around, 'false' otherwise. 
		"""
		pass

	@overload
	def isSleeping(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is sleeping, 'false' otherwise. 
		"""
		pass

	@overload
	def isDefending(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is defending another fox, 'false' otherwise. 
		"""
		pass

	@overload
	def isPouncing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is just before its leap, 'false' otherwise. 
		"""
		pass

	@overload
	def isJumping(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is jumping, 'false' otherwise. 
		"""
		pass

	@overload
	def isSneaking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fox is sneaking in preparation of an attack, 'false' otherwise. 
		"""
		pass

	pass


