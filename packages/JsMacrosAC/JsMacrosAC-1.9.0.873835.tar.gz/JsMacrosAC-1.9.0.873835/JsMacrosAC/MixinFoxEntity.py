from typing import overload
from typing import List
from typing import TypeVar

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID


class MixinFoxEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeIsAggressive(self) -> bool:
		pass

	@overload
	def invokeGetTrustedUuids(self) -> List[UUID]:
		pass

	pass


