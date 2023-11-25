from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_projectile_PersistentProjectileEntity = TypeVar("net_minecraft_entity_projectile_PersistentProjectileEntity")
PersistentProjectileEntity = net_minecraft_entity_projectile_PersistentProjectileEntity


class ArrowEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PersistentProjectileEntity) -> None:
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the particle's color of the arrow, or '-1' if the arrow has no particles. 
		"""
		pass

	@overload
	def isCritical(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the arrow will deal critical damage, 'false' otherwise. 
		"""
		pass

	@overload
	def getPiercingLevel(self) -> int:
		"""The piercing level will only be set if the arrow was fired from a crossbow with the piercing
enchantment.\n
		Since: 1.8.4 

		Returns:
			the piercing level of the arrow. 
		"""
		pass

	@overload
	def isShotFromCrossbow(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the arrow is shot from a crossbow, 'false' otherwise. 
		"""
		pass

	pass


