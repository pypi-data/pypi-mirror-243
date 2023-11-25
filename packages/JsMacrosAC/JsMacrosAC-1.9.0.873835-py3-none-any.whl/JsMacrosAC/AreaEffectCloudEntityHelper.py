from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_AreaEffectCloudEntity = TypeVar("net_minecraft_entity_AreaEffectCloudEntity")
AreaEffectCloudEntity = net_minecraft_entity_AreaEffectCloudEntity


class AreaEffectCloudEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, e: AreaEffectCloudEntity) -> None:
		pass

	@overload
	def getRadius(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the radius of this cloud. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of this cloud. 
		"""
		pass

	@overload
	def getParticleType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the id of this cloud's particles. 
		"""
		pass

	@overload
	def isWaiting(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	pass


