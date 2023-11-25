from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .BlockStateHelper import BlockStateHelper

net_minecraft_entity_mob_EndermanEntity = TypeVar("net_minecraft_entity_mob_EndermanEntity")
EndermanEntity = net_minecraft_entity_mob_EndermanEntity


class EndermanEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: EndermanEntity) -> None:
		pass

	@overload
	def isScreaming(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this enderman is screaming, 'false' otherwise. 
		"""
		pass

	@overload
	def isProvoked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this enderman was provoked by a player, 'false' otherwise. 
		"""
		pass

	@overload
	def isHoldingBlock(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this enderman is holding a block, 'false' otherwise. 
		"""
		pass

	@overload
	def getHeldBlock(self) -> BlockStateHelper:
		"""
		Since: 1.8.4 

		Returns:
			the held block of this enderman, or 'null' if it is not holding a block. 
		"""
		pass

	pass


