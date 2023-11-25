from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

net_minecraft_advancement_AdvancementProgress = TypeVar("net_minecraft_advancement_AdvancementProgress")
AdvancementProgress = net_minecraft_advancement_AdvancementProgress


class AdvancementProgressHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: AdvancementProgress) -> None:
		pass

	@overload
	def isDone(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the advancement is finished, 'false' otherwise. 
		"""
		pass

	@overload
	def isAnyObtained(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if any criteria has already been met, 'false' otherwise. 
		"""
		pass

	@overload
	def getCriteria(self) -> Mapping[str, Long]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all criteria and their completion date. 
		"""
		pass

	@overload
	def getRequirements(self) -> List[List[str]]:
		"""
		Since: 1.8.4 

		Returns:
			all requirements of this advancement. 
		"""
		pass

	@overload
	def getPercentage(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the percentage of finished requirements. 
		"""
		pass

	@overload
	def getFraction(self) -> TextHelper:
		"""
		Since: 1.8.4 

		Returns:
			the fraction of finished requirements to total requirements. 
		"""
		pass

	@overload
	def countObtainedRequirements(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of requirements criteria. 
		"""
		pass

	@overload
	def getUnobtainedCriteria(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			the amount/values of missing criteria. 
		"""
		pass

	@overload
	def getObtainedCriteria(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			the ids of the finished requirements. 
		"""
		pass

	@overload
	def getEarliestProgressObtainDate(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the earliest completion date of all criteria. 
		"""
		pass

	@overload
	def getCriterionProgress(self, criteria: str) -> float:
		"""
		Since: 1.8.4 

		Args:
			criteria: the criteria 

		Returns:
			the completion date of the given criteria or '-1' if the criteria is not met
yet. 
		"""
		pass

	@overload
	def isCriteriaObtained(self, criteria: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			criteria: the criteria 

		Returns:
			'true' if the given criteria is met, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


