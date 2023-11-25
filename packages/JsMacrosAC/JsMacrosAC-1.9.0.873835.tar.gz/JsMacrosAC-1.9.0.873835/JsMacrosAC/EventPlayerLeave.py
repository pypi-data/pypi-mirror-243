from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .PlayerListEntryHelper import PlayerListEntryHelper

net_minecraft_client_network_PlayerListEntry = TypeVar("net_minecraft_client_network_PlayerListEntry")
PlayerListEntry = net_minecraft_client_network_PlayerListEntry

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID


class EventPlayerLeave(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	UUID: str
	player: PlayerListEntryHelper

	@overload
	def __init__(self, uuid: UUID, player: PlayerListEntry) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


