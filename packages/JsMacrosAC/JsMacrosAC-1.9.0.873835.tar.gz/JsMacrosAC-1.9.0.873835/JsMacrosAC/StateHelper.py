from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .BaseHelper import BaseHelper

U = TypeVar("U")

class StateHelper(Generic[U], BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: U) -> None:
		pass

	@overload
	def toMap(self) -> Mapping[str, str]:
		"""
		Since: 1.8.4 

		Returns:
			a map of the state properties with its identifier and value. 
		"""
		pass

	@overload
	def with_(self, property: str, value: str) -> "StateHelper":
		pass

	pass


