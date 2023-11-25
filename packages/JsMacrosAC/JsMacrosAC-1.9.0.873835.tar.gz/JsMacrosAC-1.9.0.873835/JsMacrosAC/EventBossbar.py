from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .BossBarHelper import BossBarHelper

net_minecraft_client_gui_hud_ClientBossBar = TypeVar("net_minecraft_client_gui_hud_ClientBossBar")
ClientBossBar = net_minecraft_client_gui_hud_ClientBossBar

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID


class EventBossbar(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	bossBar: BossBarHelper
	uuid: str
	type: str

	@overload
	def __init__(self, type: str, uuid: UUID, bossBar: ClientBossBar) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


