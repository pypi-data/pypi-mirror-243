from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_RabbitEntity = TypeVar("net_minecraft_entity_passive_RabbitEntity")
RabbitEntity = net_minecraft_entity_passive_RabbitEntity


class RabbitEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: RabbitEntity) -> None:
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this rabbit. 
		"""
		pass

	@overload
	def isKillerBunny(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this rabbit is a killer bunny, 'false' otherwise. 
		"""
		pass

	pass


