from typing import overload
from typing import TypeVar
from .RunningContextContainer import RunningContextContainer

java_util_Comparator_xyz_wagyourtail_jsmacros_client_gui_containers_RunningContextContainer_ = TypeVar("java_util_Comparator_xyz_wagyourtail_jsmacros_client_gui_containers_RunningContextContainer_")
Comparator = java_util_Comparator_xyz_wagyourtail_jsmacros_client_gui_containers_RunningContextContainer_


class CancelScreen_RTCSort(Comparator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, arg0: RunningContextContainer, arg1: RunningContextContainer) -> int:
		pass

	pass


