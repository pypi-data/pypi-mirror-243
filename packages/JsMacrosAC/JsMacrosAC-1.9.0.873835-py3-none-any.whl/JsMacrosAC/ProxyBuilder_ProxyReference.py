from typing import overload
from typing import TypeVar
from typing import Generic

java_util_function_Function_java_lang_Object[],java_lang_Object_ = TypeVar("java_util_function_Function_java_lang_Object[],java_lang_Object_")
Function = java_util_function_Function_java_lang_Object[],java_lang_Object_

T = TypeVar("T")

class ProxyBuilder_ProxyReference(Generic[T]):
	self: T
	parent: Function

	@overload
	def __init__(self, self: T, parent: Function) -> None:
		pass

	pass


