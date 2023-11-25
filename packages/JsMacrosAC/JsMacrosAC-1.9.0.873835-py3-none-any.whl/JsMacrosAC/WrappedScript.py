from typing import overload
from typing import TypeVar
from typing import Generic
from .MethodWrapper import MethodWrapper

java_util_function_Function_xyz_wagyourtail_jsmacros_core_event_BaseEvent,xyz_wagyourtail_jsmacros_core_language_EventContainer_xyz_wagyourtail_jsmacros_core_language_BaseScriptContext____ = TypeVar("java_util_function_Function_xyz_wagyourtail_jsmacros_core_event_BaseEvent,xyz_wagyourtail_jsmacros_core_language_EventContainer_xyz_wagyourtail_jsmacros_core_language_BaseScriptContext____")
Function = java_util_function_Function_xyz_wagyourtail_jsmacros_core_event_BaseEvent,xyz_wagyourtail_jsmacros_core_language_EventContainer_xyz_wagyourtail_jsmacros_core_language_BaseScriptContext____

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
V = V


class WrappedScript(Generic[T, U, V], MethodWrapper):
	f: Function
	_async: bool

	@overload
	def __init__(self, f: Function, _async: bool) -> None:
		pass

	@overload
	def accept(self, t: T) -> None:
		pass

	@overload
	def accept(self, t: T, u: U) -> None:
		pass

	@overload
	def apply(self, t: T) -> V:
		pass

	@overload
	def apply(self, t: T, u: U) -> V:
		pass

	@overload
	def test(self, t: T) -> bool:
		pass

	@overload
	def test(self, t: T, u: U) -> bool:
		pass

	@overload
	def run(self) -> None:
		pass

	@overload
	def compare(self, o1: T, o2: T) -> int:
		pass

	@overload
	def get(self) -> V:
		pass

	pass


