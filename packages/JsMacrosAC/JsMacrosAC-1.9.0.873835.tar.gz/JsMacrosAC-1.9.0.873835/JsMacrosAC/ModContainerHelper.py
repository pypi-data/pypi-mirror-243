from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .BaseHelper import BaseHelper

T = TypeVar("T")

class ModContainerHelper(Generic[T], BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the mod's id. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the mod's name. 
		"""
		pass

	@overload
	def getDescription(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the mod's description. 
		"""
		pass

	@overload
	def getVersion(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the mod's version. 
		"""
		pass

	@overload
	def getEnv(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the environment this mod is intended for. 
		"""
		pass

	@overload
	def getAuthors(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all authors. 
		"""
		pass

	@overload
	def getDependencies(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all dependencies. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


