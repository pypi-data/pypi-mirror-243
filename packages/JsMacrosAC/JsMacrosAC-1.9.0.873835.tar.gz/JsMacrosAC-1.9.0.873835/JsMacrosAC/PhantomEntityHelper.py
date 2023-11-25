from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_PhantomEntity = TypeVar("net_minecraft_entity_mob_PhantomEntity")
PhantomEntity = net_minecraft_entity_mob_PhantomEntity


class PhantomEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PhantomEntity) -> None:
		pass

	@overload
	def getSize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the size of this phantom. 
		"""
		pass

	pass


