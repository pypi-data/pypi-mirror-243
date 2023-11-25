from typing import overload
from typing import TypeVar
from .ZombieEntityHelper import ZombieEntityHelper

net_minecraft_entity_mob_DrownedEntity = TypeVar("net_minecraft_entity_mob_DrownedEntity")
DrownedEntity = net_minecraft_entity_mob_DrownedEntity


class DrownedEntityHelper(ZombieEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: DrownedEntity) -> None:
		pass

	@overload
	def hasTrident(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this drowned is holding a trident, 'false' otherwise. 
		"""
		pass

	@overload
	def hasNautilusShell(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this drowned is holding a nautilus shell, 'false' otherwise. 
		"""
		pass

	pass


