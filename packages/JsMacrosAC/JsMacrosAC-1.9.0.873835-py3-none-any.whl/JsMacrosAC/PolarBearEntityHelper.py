from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_PolarBearEntity = TypeVar("net_minecraft_entity_passive_PolarBearEntity")
PolarBearEntity = net_minecraft_entity_passive_PolarBearEntity


class PolarBearEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PolarBearEntity) -> None:
		pass

	@overload
	def isAttacking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the polar bear is standing up to attack, 'false' otherwise. 
		"""
		pass

	pass


