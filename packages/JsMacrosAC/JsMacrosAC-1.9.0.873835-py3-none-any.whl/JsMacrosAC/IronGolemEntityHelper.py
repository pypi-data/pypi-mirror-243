from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_passive_IronGolemEntity = TypeVar("net_minecraft_entity_passive_IronGolemEntity")
IronGolemEntity = net_minecraft_entity_passive_IronGolemEntity


class IronGolemEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: IronGolemEntity) -> None:
		pass

	@overload
	def isPlayerCreated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this iron golem was created by a player, 'false' otherwise. 
		"""
		pass

	pass


