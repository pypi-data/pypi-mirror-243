from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_passive_BatEntity = TypeVar("net_minecraft_entity_passive_BatEntity")
BatEntity = net_minecraft_entity_passive_BatEntity


class BatEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BatEntity) -> None:
		pass

	@overload
	def isResting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the bat is hanging upside down, 'false' otherwise. 
		"""
		pass

	pass


