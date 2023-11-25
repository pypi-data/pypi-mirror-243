from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper
from .BlockPosHelper import BlockPosHelper

net_minecraft_entity_decoration_EndCrystalEntity = TypeVar("net_minecraft_entity_decoration_EndCrystalEntity")
EndCrystalEntity = net_minecraft_entity_decoration_EndCrystalEntity


class EndCrystalEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: EndCrystalEntity) -> None:
		pass

	@overload
	def isNatural(self) -> bool:
		"""Naturally generated end crystals will have a bedrock base, while player placed ones will
not.\n
		Since: 1.8.4 

		Returns:
			'true' if the end crystal was not placed by a player, 'false' otherwise. 
		"""
		pass

	@overload
	def getBeamTarget(self) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Returns:
			the target of the crystal's beam, or 'null' if there is none. 
		"""
		pass

	pass


