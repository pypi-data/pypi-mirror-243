from typing import overload
from typing import TypeVar

java_util_function_Supplier_java_lang_String_ = TypeVar("java_util_function_Supplier_java_lang_String_")
Supplier = java_util_function_Supplier_java_lang_String_


class Mappings_MethodData:
	name: str
	sig: Supplier

	@overload
	def __init__(self, name: str, sig: Supplier) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


