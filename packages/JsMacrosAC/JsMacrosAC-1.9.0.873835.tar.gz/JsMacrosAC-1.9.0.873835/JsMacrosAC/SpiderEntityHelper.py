from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_SpiderEntity = TypeVar("net_minecraft_entity_mob_SpiderEntity")
SpiderEntity = net_minecraft_entity_mob_SpiderEntity


class SpiderEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: SpiderEntity) -> None:
		pass

	@overload
	def isClimbing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this spider is currently climbing a wall, 'false' otherwise. 
		"""
		pass

	pass


