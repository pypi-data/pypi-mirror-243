from typing import overload
from typing import TypeVar

net_minecraft_entity_vehicle_BoatEntity_Location = TypeVar("net_minecraft_entity_vehicle_BoatEntity_Location")
BoatEntity_Location = net_minecraft_entity_vehicle_BoatEntity_Location


class MixinBoatEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getLocation(self) -> BoatEntity_Location:
		pass

	pass


