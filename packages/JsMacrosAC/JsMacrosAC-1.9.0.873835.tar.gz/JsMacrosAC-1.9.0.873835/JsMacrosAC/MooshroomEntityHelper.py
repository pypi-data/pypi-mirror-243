from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_MooshroomEntity = TypeVar("net_minecraft_entity_passive_MooshroomEntity")
MooshroomEntity = net_minecraft_entity_passive_MooshroomEntity


class MooshroomEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: MooshroomEntity) -> None:
		pass

	@overload
	def isShearable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom can be sheared, 'false' otherwise. 
		"""
		pass

	@overload
	def isRed(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom is a red mooshroom, 'false' otherwise. 
		"""
		pass

	@overload
	def isBrown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom is a brown mooshroom, 'false' otherwise. 
		"""
		pass

	pass


