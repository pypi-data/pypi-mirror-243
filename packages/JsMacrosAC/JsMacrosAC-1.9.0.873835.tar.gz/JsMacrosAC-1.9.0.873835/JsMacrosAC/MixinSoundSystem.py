from typing import overload
from typing import TypeVar

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_client_sound_SoundInstance = TypeVar("net_minecraft_client_sound_SoundInstance")
SoundInstance = net_minecraft_client_sound_SoundInstance


class MixinSoundSystem:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onPlay(self, instance: SoundInstance, info: CallbackInfo) -> None:
		pass

	pass


