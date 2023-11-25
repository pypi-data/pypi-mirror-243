from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .EntityHelper import EntityHelper

net_minecraft_entity_mob_GuardianEntity = TypeVar("net_minecraft_entity_mob_GuardianEntity")
GuardianEntity = net_minecraft_entity_mob_GuardianEntity


class GuardianEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: GuardianEntity) -> None:
		pass

	@overload
	def isElder(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this guardian is an elder guardian, 'false' otherwise. 
		"""
		pass

	@overload
	def hasTarget(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this guardian is targeting a mob, 'false' otherwise. 
		"""
		pass

	@overload
	def getTarget(self) -> EntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the target of this guardian's beam, or 'null' if it has no target. 
		"""
		pass

	@overload
	def hasSpikesRetracted(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this guardian has its spikes extended, 'false' otherwise. 
		"""
		pass

	pass


