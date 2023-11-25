from typing import overload
from typing import TypeVar

org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_ = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_")
CallbackInfoReturnable = org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class MixinChatScreen(Screen):

	@overload
	def onSendChatMessage(self, chatText: str, addToHistory: bool, cir: CallbackInfoReturnable) -> None:
		pass

	pass


