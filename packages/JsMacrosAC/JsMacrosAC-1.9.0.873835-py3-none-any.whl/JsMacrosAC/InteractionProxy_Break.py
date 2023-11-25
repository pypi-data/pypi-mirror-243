from typing import overload
from typing import TypeVar

java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_api_classes_InteractionProxy_Break_BreakBlockResult_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_api_classes_InteractionProxy_Break_BreakBlockResult_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_api_classes_InteractionProxy_Break_BreakBlockResult_

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos


class InteractionProxy_Break:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def setOverride(self, value: bool) -> None:
		pass

	@overload
	def setOverride(self, value: bool, reason: str) -> None:
		pass

	@overload
	def addCallback(self, callback: Consumer, breaking: bool) -> None:
		pass

	@overload
	def isBreaking(self) -> bool:
		pass

	@overload
	def onBreakBlock(self, pos: BlockPos, ret: bool) -> None:
		pass

	pass


