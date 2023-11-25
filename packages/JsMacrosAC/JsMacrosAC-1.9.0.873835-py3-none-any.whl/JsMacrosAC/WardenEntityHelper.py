from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_WardenEntity = TypeVar("net_minecraft_entity_mob_WardenEntity")
WardenEntity = net_minecraft_entity_mob_WardenEntity


class WardenEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: WardenEntity) -> None:
		pass

	@overload
	def getAnger(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			this warden's anger towards its active target. 
		"""
		pass

	@overload
	def isDigging(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this warden is digging into the ground, 'false' otherwise. 
		"""
		pass

	@overload
	def isEmerging(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this warden is emerging from the ground, 'false' otherwise. 
		"""
		pass

	@overload
	def isRoaring(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this warden is roaring, 'false' otherwise. 
		"""
		pass

	@overload
	def isSniffing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this warden is sniffing, 'false' otherwise. 
		"""
		pass

	@overload
	def isChargingSonicBoom(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this warden is charging its sonic boom attack, 'false' otherwise. 
		"""
		pass

	pass


