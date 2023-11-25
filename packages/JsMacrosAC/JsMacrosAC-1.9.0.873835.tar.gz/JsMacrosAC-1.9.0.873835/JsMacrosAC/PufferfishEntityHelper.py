from typing import overload
from typing import TypeVar
from .FishEntityHelper import FishEntityHelper

net_minecraft_entity_passive_PufferfishEntity = TypeVar("net_minecraft_entity_passive_PufferfishEntity")
PufferfishEntity = net_minecraft_entity_passive_PufferfishEntity


class PufferfishEntityHelper(FishEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PufferfishEntity) -> None:
		pass

	@overload
	def getSize(self) -> int:
		"""A state of 0 means the fish is deflated, a state of 1 means the fish is inflated and a state
of 2 means the fish is fully inflated.\n
		Since: 1.8.4 

		Returns:
			the puff state of this pufferfish. 
		"""
		pass

	pass


