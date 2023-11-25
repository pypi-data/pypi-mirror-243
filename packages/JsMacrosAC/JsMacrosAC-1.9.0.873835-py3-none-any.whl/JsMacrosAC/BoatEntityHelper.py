from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper
from .BlockHelper import BlockHelper

net_minecraft_entity_vehicle_BoatEntity = TypeVar("net_minecraft_entity_vehicle_BoatEntity")
BoatEntity = net_minecraft_entity_vehicle_BoatEntity


class BoatEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BoatEntity) -> None:
		pass

	@overload
	def isChestBoat(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the boat is a chest boat, 'false' otherwise. 
		"""
		pass

	@overload
	def getBoatBlockType(self) -> BlockHelper:
		"""
		Since: 1.8.4 

		Returns:
			the boat's plank type. 
		"""
		pass

	@overload
	def getBoatType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the boat's material. 
		"""
		pass

	@overload
	def isInWater(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the boat is on top of water, 'false' otherwise. 
		"""
		pass

	@overload
	def isOnLand(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the boat is on land, 'false' otherwise. 
		"""
		pass

	@overload
	def isUnderwater(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the boat is underwater, 'false' otherwise. 
		"""
		pass

	@overload
	def isInAir(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the boat is in the air, 'false' otherwise. 
		"""
		pass

	pass


