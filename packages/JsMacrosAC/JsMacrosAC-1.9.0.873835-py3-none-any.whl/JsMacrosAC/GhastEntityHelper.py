from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_GhastEntity = TypeVar("net_minecraft_entity_mob_GhastEntity")
GhastEntity = net_minecraft_entity_mob_GhastEntity


class GhastEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: GhastEntity) -> None:
		pass

	@overload
	def isShooting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this ghast is currently about to shoot a fireball, 'false' otherwise. 
		"""
		pass

	pass


