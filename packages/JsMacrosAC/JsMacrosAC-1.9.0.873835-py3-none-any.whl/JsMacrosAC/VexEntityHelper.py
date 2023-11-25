from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_VexEntity = TypeVar("net_minecraft_entity_mob_VexEntity")
VexEntity = net_minecraft_entity_mob_VexEntity


class VexEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: VexEntity) -> None:
		pass

	@overload
	def isCharging(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this vex is currently charging at its target, 'false' otherwise. 
		"""
		pass

	pass


