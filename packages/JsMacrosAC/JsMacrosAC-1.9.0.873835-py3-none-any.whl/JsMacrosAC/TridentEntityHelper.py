from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_projectile_TridentEntity = TypeVar("net_minecraft_entity_projectile_TridentEntity")
TridentEntity = net_minecraft_entity_projectile_TridentEntity


class TridentEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: TridentEntity) -> None:
		pass

	@overload
	def hasLoyalty(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the trident is enchanted with loyalty, 'false' otherwise. 
		"""
		pass

	@overload
	def isEnchanted(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the trident is enchanted, 'false' otherwise. 
		"""
		pass

	pass


