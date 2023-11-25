from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_AxolotlEntity = TypeVar("net_minecraft_entity_passive_AxolotlEntity")
AxolotlEntity = net_minecraft_entity_passive_AxolotlEntity


class AxolotlEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: AxolotlEntity) -> None:
		pass

	@overload
	def getVariantId(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the id of this axolotl's variant. 
		"""
		pass

	@overload
	def getVariantName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this axolotl's variant. 
		"""
		pass

	@overload
	def isPlayingDead(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the axolotl is playing dead, 'false' otherwise. 
		"""
		pass

	@overload
	def isFromBucket(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the axolotl came from a bucket, 'false' otherwise. 
		"""
		pass

	pass


