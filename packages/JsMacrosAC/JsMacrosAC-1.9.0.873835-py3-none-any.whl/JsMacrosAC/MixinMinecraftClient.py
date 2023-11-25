from typing import overload
from typing import TypeVar

net_minecraft_client_network_ClientPlayerInteractionManager = TypeVar("net_minecraft_client_network_ClientPlayerInteractionManager")
ClientPlayerInteractionManager = net_minecraft_client_network_ClientPlayerInteractionManager

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_world_ClientWorld = TypeVar("net_minecraft_client_world_ClientWorld")
ClientWorld = net_minecraft_client_world_ClientWorld


class MixinMinecraftClient:
	currentScreen: Screen
	interactionManager: ClientPlayerInteractionManager

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def setScreen(self, screen: Screen) -> None:
		pass

	@overload
	def onJoinWorld(self, world: ClientWorld, info: CallbackInfo) -> None:
		pass

	@overload
	def onOpenScreen(self, screen: Screen, info: CallbackInfo) -> None:
		pass

	@overload
	def afterOpenScreen(self, screen: Screen, info: CallbackInfo) -> None:
		pass

	@overload
	def onDisconnect(self, s: Screen, info: CallbackInfo) -> None:
		pass

	pass


