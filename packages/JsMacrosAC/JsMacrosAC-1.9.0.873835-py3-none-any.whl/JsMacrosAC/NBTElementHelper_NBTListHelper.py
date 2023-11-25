from typing import overload
from typing import TypeVar
from .NBTElementHelper import NBTElementHelper

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID


class NBTElementHelper_NBTListHelper(NBTElementHelper):
	"""
	Since: 1.5.1 
	"""

	@overload
	def isPossiblyUUID(self) -> bool:
		"""
		Since: 1.8.3 
		"""
		pass

	@overload
	def asUUID(self) -> UUID:
		"""
		Since: 1.8.3 
		"""
		pass

	@overload
	def length(self) -> int:
		"""
		Since: 1.5.1 
		"""
		pass

	@overload
	def get(self, index: int) -> NBTElementHelper:
		"""
		Since: 1.5.1 
		"""
		pass

	@overload
	def getHeldType(self) -> int:
		"""
		Since: 1.5.1 
		"""
		pass

	pass


