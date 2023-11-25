from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .AdvancementProgressHelper import AdvancementProgressHelper

net_minecraft_advancement_PlacedAdvancement = TypeVar("net_minecraft_advancement_PlacedAdvancement")
PlacedAdvancement = net_minecraft_advancement_PlacedAdvancement


class AdvancementHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PlacedAdvancement) -> None:
		pass

	@overload
	def getParent(self) -> "AdvancementHelper":
		"""
		Since: 1.8.4 

		Returns:
			the parent advancement or 'null' if there is none. 
		"""
		pass

	@overload
	def getChildren(self) -> List["AdvancementHelper"]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all child advancements. 
		"""
		pass

	@overload
	def getRequirements(self) -> List[List[str]]:
		"""
		Since: 1.8.4 

		Returns:
			the requirements of this advancement. 
		"""
		pass

	@overload
	def getRequirementCount(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of requirements. 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of this advancement. 
		"""
		pass

	@overload
	def getExperience(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the experience awarded by this advancement. 
		"""
		pass

	@overload
	def getLoot(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			the loot table ids for this advancement's rewards. 
		"""
		pass

	@overload
	def getRecipes(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			the recipes unlocked through this advancement. 
		"""
		pass

	@overload
	def getProgress(self) -> AdvancementProgressHelper:
		"""
		Since: 1.8.4 

		Returns:
			the progress. 
		"""
		pass

	@overload
	def toJson(self) -> str:
		"""
		Since: 1.9.0 

		Returns:
			the json string of this advancement. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


