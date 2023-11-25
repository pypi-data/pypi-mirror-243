from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_PigEntity = TypeVar("net_minecraft_entity_passive_PigEntity")
PigEntity = net_minecraft_entity_passive_PigEntity


class PigEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PigEntity) -> None:
		pass

	@overload
	def isSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this pig is saddled, 'false' otherwise. 
		"""
		pass

	pass


