from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_passive_AllayEntity = TypeVar("net_minecraft_entity_passive_AllayEntity")
AllayEntity = net_minecraft_entity_passive_AllayEntity


class AllayEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: AllayEntity) -> None:
		pass

	@overload
	def isDancing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this allay is dancing, 'false' otherwise. 
		"""
		pass

	@overload
	def canDuplicate(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this allay can be duplicated, 'false' otherwise. 
		"""
		pass

	@overload
	def isHoldingItem(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this allay is holding a item, 'false' otherwise. 
		"""
		pass

	pass


