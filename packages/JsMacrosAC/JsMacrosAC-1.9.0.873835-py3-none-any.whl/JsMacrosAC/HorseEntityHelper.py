from typing import overload
from typing import TypeVar
from .AbstractHorseEntityHelper import AbstractHorseEntityHelper

net_minecraft_entity_passive_HorseEntity = TypeVar("net_minecraft_entity_passive_HorseEntity")
HorseEntity = net_minecraft_entity_passive_HorseEntity


class HorseEntityHelper(AbstractHorseEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: HorseEntity) -> None:
		pass

	@overload
	def getVariant(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this horse. 
		"""
		pass

	pass


