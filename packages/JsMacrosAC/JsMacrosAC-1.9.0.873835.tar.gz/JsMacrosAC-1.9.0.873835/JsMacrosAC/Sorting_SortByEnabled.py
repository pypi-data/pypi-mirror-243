from typing import overload
from typing import TypeVar
from .ScriptTrigger import ScriptTrigger

java_util_Comparator_xyz_wagyourtail_jsmacros_core_config_ScriptTrigger_ = TypeVar("java_util_Comparator_xyz_wagyourtail_jsmacros_core_config_ScriptTrigger_")
Comparator = java_util_Comparator_xyz_wagyourtail_jsmacros_core_config_ScriptTrigger_


class Sorting_SortByEnabled(Comparator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, a: ScriptTrigger, b: ScriptTrigger) -> int:
		pass

	pass


