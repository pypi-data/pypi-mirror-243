from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_CreeperEntity = TypeVar("net_minecraft_entity_mob_CreeperEntity")
CreeperEntity = net_minecraft_entity_mob_CreeperEntity


class CreeperEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: CreeperEntity) -> None:
		pass

	@overload
	def isCharged(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the creeper is charged, 'false' otherwise. 
		"""
		pass

	@overload
	def isIgnited(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the creeper has been ignited, 'false' otherwise. 
		"""
		pass

	@overload
	def getFuseChange(self) -> int:
		"""A negative value means the creeper is currently defusing, while a positive value means the
creeper is currently charging up.\n
		Since: 1.8.4 

		Returns:
			the change in fuse every tick. 
		"""
		pass

	@overload
	def getFuseTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the time the creeper has been charging up. 
		"""
		pass

	@overload
	def getMaxFuseTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum time the creeper can be charged for before exploding. 
		"""
		pass

	@overload
	def getRemainingFuseTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining time until the creeper explodes with the current fuse time, or '-1' if the creeper is not about to explode. 
		"""
		pass

	pass


