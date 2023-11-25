from typing import overload
from typing import TypeVar
from typing import Mapping
from .IBossBarHud import IBossBarHud

net_minecraft_client_gui_hud_ClientBossBar = TypeVar("net_minecraft_client_gui_hud_ClientBossBar")
ClientBossBar = net_minecraft_client_gui_hud_ClientBossBar

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID


class MixinBossBarHud(IBossBarHud):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_GetBossBars(self) -> Mapping[UUID, ClientBossBar]:
		pass

	pass


