from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .BlockPosHelper import BlockPosHelper

net_minecraft_entity_passive_DolphinEntity = TypeVar("net_minecraft_entity_passive_DolphinEntity")
DolphinEntity = net_minecraft_entity_passive_DolphinEntity


class DolphinEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: DolphinEntity) -> None:
		pass

	@overload
	def hasFish(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the dolphin has a fish in its mouth, 'false' otherwise. 
		"""
		pass

	@overload
	def getTreasurePos(self) -> BlockPosHelper:
		"""The position will be 0 0 0 by default.\n
		Since: 1.8.4 

		Returns:
			the position of the treasure the dolphin is looking for. 
		"""
		pass

	@overload
	def getMoistness(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the moisture level of the dolphin. 
		"""
		pass

	pass


