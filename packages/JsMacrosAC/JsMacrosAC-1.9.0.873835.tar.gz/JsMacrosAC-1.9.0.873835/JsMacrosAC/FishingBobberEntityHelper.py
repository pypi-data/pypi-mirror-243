from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_projectile_FishingBobberEntity = TypeVar("net_minecraft_entity_projectile_FishingBobberEntity")
FishingBobberEntity = net_minecraft_entity_projectile_FishingBobberEntity


class FishingBobberEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FishingBobberEntity) -> None:
		pass

	@overload
	def hasCaughtFish(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if a fish has been caught, 'false' otherwise. 
		"""
		pass

	@overload
	def isInOpenWater(self) -> bool:
		"""When in open water the player can get treasures from fishing.\n
		Since: 1.8.4 

		Returns:
			'true' if the bobber is in open water, 'false' otherwise. 
		"""
		pass

	@overload
	def hasEntityHooked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the bobber has an entity hooked, 'false' otherwise. 
		"""
		pass

	@overload
	def getHookedEntity(self) -> EntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the hooked entity, or 'null' if there is no entity hooked. 
		"""
		pass

	pass


