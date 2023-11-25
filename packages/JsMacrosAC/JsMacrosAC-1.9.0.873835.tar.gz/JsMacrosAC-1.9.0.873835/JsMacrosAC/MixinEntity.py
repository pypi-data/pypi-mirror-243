from typing import overload
from typing import TypeVar
from .IMixinEntity import IMixinEntity

org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_ = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_")
CallbackInfoReturnable = org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_


class MixinEntity(IMixinEntity):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_setGlowingColor(self, glowingColor: int) -> None:
		pass

	@overload
	def jsmacros_resetColor(self) -> None:
		pass

	@overload
	def getTeamColorValue(self, ci: CallbackInfoReturnable) -> None:
		pass

	@overload
	def jsmacros_setForceGlowing(self, glowing: int) -> None:
		pass

	@overload
	def isGlowing(self, cir: CallbackInfoReturnable) -> None:
		pass

	pass


