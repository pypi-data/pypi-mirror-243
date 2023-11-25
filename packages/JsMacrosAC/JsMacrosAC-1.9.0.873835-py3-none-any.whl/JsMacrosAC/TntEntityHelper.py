from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_TntEntity = TypeVar("net_minecraft_entity_TntEntity")
TntEntity = net_minecraft_entity_TntEntity


class TntEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: TntEntity) -> None:
		pass

	@overload
	def getRemainingTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining time until this TNT explodes. 
		"""
		pass

	pass


