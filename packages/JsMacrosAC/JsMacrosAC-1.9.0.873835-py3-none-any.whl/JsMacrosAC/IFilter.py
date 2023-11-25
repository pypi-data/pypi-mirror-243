from typing import overload
from typing import TypeVar
from typing import Generic

java_util_function_Function_T,java_lang_Boolean_ = TypeVar("java_util_function_Function_T,java_lang_Boolean_")
Function = java_util_function_Function_T,java_lang_Boolean_

T = TypeVar("T")

class IFilter(Function, Generic[T]):
	"""
	Since: 1.6.5 
	"""

	@overload
	def apply(self, t: T) -> bool:
		pass

	pass


