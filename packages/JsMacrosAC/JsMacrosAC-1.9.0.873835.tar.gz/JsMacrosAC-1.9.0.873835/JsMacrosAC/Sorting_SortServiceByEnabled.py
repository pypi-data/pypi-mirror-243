from typing import overload
from typing import TypeVar

java_util_Comparator_java_lang_String_ = TypeVar("java_util_Comparator_java_lang_String_")
Comparator = java_util_Comparator_java_lang_String_


class Sorting_SortServiceByEnabled(Comparator):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, a: str, b: str) -> int:
		pass

	pass


