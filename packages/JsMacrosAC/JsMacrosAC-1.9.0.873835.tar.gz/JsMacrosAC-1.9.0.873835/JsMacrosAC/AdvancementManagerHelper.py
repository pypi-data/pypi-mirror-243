from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .AdvancementHelper import AdvancementHelper
from .AdvancementProgressHelper import AdvancementProgressHelper

net_minecraft_advancement_AdvancementManager = TypeVar("net_minecraft_advancement_AdvancementManager")
AdvancementManager = net_minecraft_advancement_AdvancementManager


class AdvancementManagerHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, advancementManager: AdvancementManager) -> None:
		pass

	@overload
	def getAdvancementsForIdentifiers(self) -> Mapping[str, AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all advancement ids and their advancement. 
		"""
		pass

	@overload
	def getAdvancements(self) -> List[AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all advancements. 
		"""
		pass

	@overload
	def getStartedAdvancements(self) -> List[AdvancementHelper]:
		"""Started advancements are advancements that have been started, so at least one task has been
completed so far, but not fully completed.\n
		Since: 1.8.4 

		Returns:
			a list of all started advancements. 
		"""
		pass

	@overload
	def getMissingAdvancements(self) -> List[AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all missing advancements. 
		"""
		pass

	@overload
	def getCompletedAdvancements(self) -> List[AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all completed advancements. 
		"""
		pass

	@overload
	def getRootAdvancements(self) -> List[AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all the root advancements. 
		"""
		pass

	@overload
	def getSubAdvancements(self) -> List[AdvancementHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all advancements that are not a root. 
		"""
		pass

	@overload
	def getAdvancement(self, identifier: str) -> AdvancementHelper:
		"""
		Since: 1.8.4 

		Args:
			identifier: the identifier of the advancement 

		Returns:
			the advancement for the given identifier. 
		"""
		pass

	@overload
	def getAdvancementsProgress(self) -> Mapping[AdvancementHelper, AdvancementProgressHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all advancements and their progress. 
		"""
		pass

	@overload
	def getAdvancementProgress(self, identifier: str) -> AdvancementProgressHelper:
		"""
		Since: 1.8.4 

		Returns:
			the progress of the given advancement. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


