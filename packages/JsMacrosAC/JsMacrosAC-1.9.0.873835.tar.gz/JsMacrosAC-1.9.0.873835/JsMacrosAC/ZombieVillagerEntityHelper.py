from typing import overload
from typing import TypeVar
from .ZombieEntityHelper import ZombieEntityHelper

net_minecraft_entity_mob_ZombieVillagerEntity = TypeVar("net_minecraft_entity_mob_ZombieVillagerEntity")
ZombieVillagerEntity = net_minecraft_entity_mob_ZombieVillagerEntity


class ZombieVillagerEntityHelper(ZombieEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ZombieVillagerEntity) -> None:
		pass

	@overload
	def isConvertingToVillager(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this zombie villager is currently being converted back to a villager, 'false' otherwise. 
		"""
		pass

	@overload
	def getVillagerBiomeType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the type of biome the villager belonged to it was converted to a zombie. 
		"""
		pass

	@overload
	def getProfession(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the profession of the villager before it was converted to a zombie. 
		"""
		pass

	@overload
	def getLevel(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the level of the villager before it was converted to a zombie. 
		"""
		pass

	pass


