from typing import overload
from typing import TypeVar

net_minecraft_util_hit_HitResult = TypeVar("net_minecraft_util_hit_HitResult")
HitResult = net_minecraft_util_hit_HitResult

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos


class InteractionProxy_Target:
	checkDistance: bool
	clearIfOutOfRange: bool
	checkAir: bool
	clearIfIsAir: bool
	checkShape: bool
	clearIfEmptyShape: bool

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def resetChecks(self) -> None:
		pass

	@overload
	def setTargetBlock(self, pos: BlockPos, direction: int) -> None:
		pass

	@overload
	def setTarget(self, value: HitResult) -> None:
		pass

	@overload
	def setTargetMissed(self) -> None:
		pass

	@overload
	def hasOverride(self) -> bool:
		pass

	@overload
	def onUpdate(self, tickDelta: float, ci: CallbackInfo) -> None:
		pass

	@overload
	def isInRange(self, tickDelta: float) -> bool:
		pass

	pass


