from typing import overload
from typing import List
from typing import TypeVar
from typing import Any
from .MobEntityHelper import MobEntityHelper
from .EntityHelper import EntityHelper

net_minecraft_entity_boss_dragon_EnderDragonEntity = TypeVar("net_minecraft_entity_boss_dragon_EnderDragonEntity")
EnderDragonEntity = net_minecraft_entity_boss_dragon_EnderDragonEntity


class EnderDragonEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: EnderDragonEntity) -> None:
		pass

	@overload
	def getPhase(self) -> str:
		"""The phases are as follows: 
'HoldingPattern' , 'StrafePlayer' , 'LandingApproach' , 'Landing' , 'Takeoff' , 'SittingFlaming' , 'SittingScanning' , 'SittingAttacking' , 'ChargingPlayer' , 'Dying' , 'Hover'\n
		Since: 1.8.4 

		Returns:
			the current phase of the dragon. 
		"""
		pass

	@overload
	def getBodyPart(self, index: int) -> EntityHelper:
		"""
		Since: 1.8.4 

		Args:
			index: the index of the dragon's body part to get 

		Returns:
			the specified body part of the dragon. 
		"""
		pass

	@overload
	def getBodyParts(self) -> List[Any]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all body parts of the dragon. 
		"""
		pass

	@overload
	def getBodyParts(self, name: str) -> List[Any]:
		"""The name can be either 'head' , 'neck' , 'body' , 'tail' or 'wing' .\n
		Since: 1.8.4 

		Args:
			name: the name of the body part to get 

		Returns:
			a list of all body parts of the dragon with the specified name. 
		"""
		pass

	pass


