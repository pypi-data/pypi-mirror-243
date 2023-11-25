from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_BlazeEntity = TypeVar("net_minecraft_entity_mob_BlazeEntity")
BlazeEntity = net_minecraft_entity_mob_BlazeEntity


class BlazeEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BlazeEntity) -> None:
		pass

	@overload
	def isOnFire(self) -> bool:
		"""A blaze can only shoot fireballs when it's on fire.\n
		Since: 1.8.4 

		Returns:
			'true' if the blaze is on fire, 'false' otherwise. 
		"""
		pass

	pass


