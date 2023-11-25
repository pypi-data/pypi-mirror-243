from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_boss_WitherEntity = TypeVar("net_minecraft_entity_boss_WitherEntity")
WitherEntity = net_minecraft_entity_boss_WitherEntity


class WitherEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: WitherEntity) -> None:
		pass

	@overload
	def getRemainingInvulnerableTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the time in ticks the wither will be invulnerable for. 
		"""
		pass

	@overload
	def isInvulnerable(self) -> bool:
		"""The wither will only be invulnerable, by default for 220 ticks, when summoned.\n
		Since: 1.8.4 

		Returns:
			'true' if the wither is invulnerable, 'false' otherwise. 
		"""
		pass

	@overload
	def isFirstPhase(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the wither is in its first phase, 'false' otherwise. 
		"""
		pass

	@overload
	def isSecondPhase(self) -> bool:
		"""In the second phase the wither will be invulnerable to projectiles and starts going down
towards the player.\n
		Since: 1.8.4 

		Returns:
			'true' if the wither is in its second phase, 'false' otherwise. 
		"""
		pass

	pass


