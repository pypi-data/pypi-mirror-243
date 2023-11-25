from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_passive_SnowGolemEntity = TypeVar("net_minecraft_entity_passive_SnowGolemEntity")
SnowGolemEntity = net_minecraft_entity_passive_SnowGolemEntity


class SnowGolemEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: SnowGolemEntity) -> None:
		pass

	@overload
	def hasPumpkin(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the snow golem has a pumpkin on its head, 'false' otherwise. 
		"""
		pass

	@overload
	def isShearable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this snow golem can be sheared, 'false' otherwise. 
		"""
		pass

	pass


