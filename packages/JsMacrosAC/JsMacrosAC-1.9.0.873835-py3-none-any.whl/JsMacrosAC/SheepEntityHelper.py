from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper
from .DyeColorHelper import DyeColorHelper

net_minecraft_entity_passive_SheepEntity = TypeVar("net_minecraft_entity_passive_SheepEntity")
SheepEntity = net_minecraft_entity_passive_SheepEntity


class SheepEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: SheepEntity) -> None:
		pass

	@overload
	def isSheared(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this sheep is sheared, 'false' otherwise. 
		"""
		pass

	@overload
	def isShearable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this sheep can be sheared, 'false' otherwise. 
		"""
		pass

	@overload
	def getColor(self) -> DyeColorHelper:
		"""
		Since: 1.8.4 

		Returns:
			the color of this sheep. 
		"""
		pass

	@overload
	def isJeb(self) -> bool:
		"""Sheep named 'jeb_' will cycle through all colors when rendered. If sheared, they will
drop their original colored wool.\n
		Since: 1.8.4 

		Returns:
			'true' if the sheep has a rainbow overlay, 'false' otherwise. 
		"""
		pass

	pass


