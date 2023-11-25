from typing import overload
from typing import TypeVar
from .IllagerEntityHelper import IllagerEntityHelper

net_minecraft_entity_mob_PillagerEntity = TypeVar("net_minecraft_entity_mob_PillagerEntity")
PillagerEntity = net_minecraft_entity_mob_PillagerEntity


class PillagerEntityHelper(IllagerEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PillagerEntity) -> None:
		pass

	@overload
	def isCaptain(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this pillager is a captain, 'false' otherwise. 
		"""
		pass

	pass


