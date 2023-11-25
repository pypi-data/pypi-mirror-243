from typing import overload
from typing import List
from typing import Any
from .ModContainerHelper import ModContainerHelper


class ModLoader:
	"""
	Since: 1.8.4 
	"""

	@overload
	def isDevEnv(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the game is running in a development environment, 'false' otherwise. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the current mod loader. 
		"""
		pass

	@overload
	def getLoadedMods(self) -> List[Any]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all loaded mods. 
		"""
		pass

	@overload
	def isModLoaded(self, modId: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			modId: the mod id to check 

		Returns:
			'true' if the mod with the given id is loaded, 'false' otherwise. 
		"""
		pass

	@overload
	def getMod(self, modId: str) -> ModContainerHelper:
		"""
		Since: 1.8.4 

		Args:
			modId: the mod id 

		Returns:
			the mod container for the given id or 'null' if the mod is not loaded. 
		"""
		pass

	pass


