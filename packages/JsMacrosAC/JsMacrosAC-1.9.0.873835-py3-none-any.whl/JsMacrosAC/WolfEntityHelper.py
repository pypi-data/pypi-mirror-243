from typing import overload
from typing import TypeVar
from .TameableEntityHelper import TameableEntityHelper
from .DyeColorHelper import DyeColorHelper

net_minecraft_entity_passive_WolfEntity = TypeVar("net_minecraft_entity_passive_WolfEntity")
WolfEntity = net_minecraft_entity_passive_WolfEntity


class WolfEntityHelper(TameableEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: WolfEntity) -> None:
		pass

	@overload
	def isBegging(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this wolf is tamed and the player has either a bone or meat in one of
their hands, 'false' otherwise. 
		"""
		pass

	@overload
	def getCollarColor(self) -> DyeColorHelper:
		"""
		Since: 1.8.4 

		Returns:
			the color of this wolf's collar. 
		"""
		pass

	@overload
	def isAngry(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this wolf is angry, 'false' otherwise. 
		"""
		pass

	@overload
	def isWet(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this wolf is wet, 'false' otherwise. 
		"""
		pass

	pass


