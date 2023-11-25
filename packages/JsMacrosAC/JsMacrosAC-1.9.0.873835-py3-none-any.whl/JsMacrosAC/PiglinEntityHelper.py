from typing import overload
from typing import TypeVar
from .AbstractPiglinEntityHelper import AbstractPiglinEntityHelper

net_minecraft_entity_mob_PiglinEntity = TypeVar("net_minecraft_entity_mob_PiglinEntity")
PiglinEntity = net_minecraft_entity_mob_PiglinEntity


class PiglinEntityHelper(AbstractPiglinEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PiglinEntity) -> None:
		pass

	@overload
	def isWandering(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin is doing nothing special, 'false' otherwise. 
		"""
		pass

	@overload
	def isDancing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin is dancing to music, 'false' otherwise. 
		"""
		pass

	@overload
	def isAdmiring(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin is admiring an item, 'false' otherwise. 
		"""
		pass

	@overload
	def isMeleeAttacking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin is attacking another entity, 'false' otherwise. 
		"""
		pass

	@overload
	def isChargingCrossbow(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin is currently charging its crossbow, 'false' otherwise. 
		"""
		pass

	@overload
	def hasCrossbowReady(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this piglin has its crossbow fully charged, 'false' otherwise. 
		"""
		pass

	pass


