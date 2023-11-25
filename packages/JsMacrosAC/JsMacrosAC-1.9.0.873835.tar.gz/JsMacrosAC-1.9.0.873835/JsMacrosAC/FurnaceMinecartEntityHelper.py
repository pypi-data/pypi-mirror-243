from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_vehicle_FurnaceMinecartEntity = TypeVar("net_minecraft_entity_vehicle_FurnaceMinecartEntity")
FurnaceMinecartEntity = net_minecraft_entity_vehicle_FurnaceMinecartEntity


class FurnaceMinecartEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FurnaceMinecartEntity) -> None:
		pass

	@overload
	def isPowered(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'' true if the furnace minecart is powered, 'false' otherwise. 
		"""
		pass

	pass


