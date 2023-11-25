from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_GoatEntity = TypeVar("net_minecraft_entity_passive_GoatEntity")
GoatEntity = net_minecraft_entity_passive_GoatEntity


class GoatEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: GoatEntity) -> None:
		pass

	@overload
	def isScreaming(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this goat is currently screaming, 'false' otherwise. 
		"""
		pass

	@overload
	def hasLeftHorn(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this goat has its left horn still left, 'false' otherwise. 
		"""
		pass

	@overload
	def hasRightHorn(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this goat has its right horn still left, 'false' otherwise. 
		"""
		pass

	@overload
	def hasHorns(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this goat still has a horn, 'false' otherwise. 
		"""
		pass

	pass


