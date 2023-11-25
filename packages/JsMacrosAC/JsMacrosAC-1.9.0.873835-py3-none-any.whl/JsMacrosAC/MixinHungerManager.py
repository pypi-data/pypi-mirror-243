from typing import overload
from typing import TypeVar

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo


class MixinHungerManager:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onSetFoodLevel(self, foodLevel: int, info: CallbackInfo) -> None:
		pass

	pass


