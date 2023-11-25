from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

net_minecraft_entity_passive_PandaEntity = TypeVar("net_minecraft_entity_passive_PandaEntity")
PandaEntity = net_minecraft_entity_passive_PandaEntity


class PandaEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PandaEntity) -> None:
		pass

	@overload
	def getMainGene(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the id of this panda's main gene. 
		"""
		pass

	@overload
	def getMainGeneName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this panda's main gene. 
		"""
		pass

	@overload
	def isMainGeneRecessive(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's main gene is recessive, 'false' otherwise. 
		"""
		pass

	@overload
	def getHiddenGene(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the id of this panda's hidden gene. 
		"""
		pass

	@overload
	def getHiddenGeneName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this panda's hidden gene. 
		"""
		pass

	@overload
	def isHiddenGeneRecessive(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's hidden gene is recessive, 'false' otherwise. 
		"""
		pass

	@overload
	def isIdle(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is idling, 'false' otherwise. 
		"""
		pass

	@overload
	def isSneezing(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is currently sneezing, 'false' otherwise. 
		"""
		pass

	@overload
	def isPlaying(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is playing, 'false' otherwise. 
		"""
		pass

	@overload
	def isSitting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is sitting, 'false' otherwise. 
		"""
		pass

	@overload
	def isLyingOnBack(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is lying on its back, 'false' otherwise. 
		"""
		pass

	@overload
	def isLazy(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him lazy, 'false' otherwise. 
		"""
		pass

	@overload
	def isWorried(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him worried, 'false' otherwise. 
		"""
		pass

	@overload
	def isScaredByThunderstorm(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda is scared by an active thunderstorm, 'false' otherwise. 
		"""
		pass

	@overload
	def isPlayful(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him playful, 'false' otherwise. 
		"""
		pass

	@overload
	def isBrown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him brown, 'false' otherwise. 
		"""
		pass

	@overload
	def isWeak(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him weak, 'false' otherwise. 
		"""
		pass

	@overload
	def isAttacking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this panda's genes make him aggressive, 'false' otherwise. 
		"""
		pass

	pass


