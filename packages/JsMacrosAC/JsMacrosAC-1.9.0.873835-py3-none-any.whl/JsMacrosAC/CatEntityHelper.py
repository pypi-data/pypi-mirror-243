from typing import overload
from typing import TypeVar
from .TameableEntityHelper import TameableEntityHelper
from .DyeColorHelper import DyeColorHelper

net_minecraft_entity_passive_CatEntity = TypeVar("net_minecraft_entity_passive_CatEntity")
CatEntity = net_minecraft_entity_passive_CatEntity


class CatEntityHelper(TameableEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: CatEntity) -> None:
		pass

	@overload
	def isSleeping(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this cat is sleeping, 'false' otherwise. 
		"""
		pass

	@overload
	def getCollarColor(self) -> DyeColorHelper:
		"""
		Since: 1.8.4 

		Returns:
			the color of this cat's collar. 
		"""
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this cat. 
		"""
		pass

	pass


