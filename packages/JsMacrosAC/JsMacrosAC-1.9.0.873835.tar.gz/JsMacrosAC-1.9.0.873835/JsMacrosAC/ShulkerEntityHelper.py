from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .DirectionHelper import DirectionHelper
from .DyeColorHelper import DyeColorHelper

net_minecraft_entity_mob_ShulkerEntity = TypeVar("net_minecraft_entity_mob_ShulkerEntity")
ShulkerEntity = net_minecraft_entity_mob_ShulkerEntity


class ShulkerEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ShulkerEntity) -> None:
		pass

	@overload
	def isClosed(self) -> bool:
		pass

	@overload
	def getAttachedSide(self) -> DirectionHelper:
		pass

	@overload
	def getColor(self) -> DyeColorHelper:
		pass

	pass


