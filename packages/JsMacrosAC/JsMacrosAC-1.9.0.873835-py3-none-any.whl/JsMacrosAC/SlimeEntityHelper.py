from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

net_minecraft_entity_mob_SlimeEntity = TypeVar("net_minecraft_entity_mob_SlimeEntity")
SlimeEntity = net_minecraft_entity_mob_SlimeEntity


class SlimeEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: SlimeEntity) -> None:
		pass

	@overload
	def getSize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the size of this slime. 
		"""
		pass

	@overload
	def isSmall(self) -> bool:
		"""Small slimes, with a size less than 1, don't attack the player.\n
		Since: 1.8.4 

		Returns:
			'true' if this slime is small, 'false' otherwise. 
		"""
		pass

	pass


