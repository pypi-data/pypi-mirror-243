from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .Option import Option

java_lang_reflect_Field = TypeVar("java_lang_reflect_Field")
Field = java_lang_reflect_Field

T = TypeVar("T")
java_lang_reflect_Method = TypeVar("java_lang_reflect_Method")
Method = java_lang_reflect_Method


class SettingsOverlay_SettingField(Generic[T]):
	type: Class
	option: Option

	@overload
	def __init__(self, option: Option, containingClass: object, f: Field, getter: Method, setter: Method, type: Class) -> None:
		pass

	@overload
	def set(self, o: T) -> None:
		pass

	@overload
	def get(self) -> T:
		pass

	@overload
	def hasOptions(self) -> bool:
		pass

	@overload
	def getOptions(self) -> List[T]:
		pass

	@overload
	def isSimple(self) -> bool:
		pass

	pass


