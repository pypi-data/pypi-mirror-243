from typing import overload
from typing import TypeVar

net_minecraft_entity_boss_BossBar_Style = TypeVar("net_minecraft_entity_boss_BossBar_Style")
BossBar_Style = net_minecraft_entity_boss_BossBar_Style

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_network_packet_s2c_play_BossBarS2CPacket_Consumer = TypeVar("net_minecraft_network_packet_s2c_play_BossBarS2CPacket_Consumer")
BossBarS2CPacket_Consumer = net_minecraft_network_packet_s2c_play_BossBarS2CPacket_Consumer

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID

net_minecraft_entity_boss_BossBar_Color = TypeVar("net_minecraft_entity_boss_BossBar_Color")
BossBar_Color = net_minecraft_entity_boss_BossBar_Color


class BossBarConsumer(BossBarS2CPacket_Consumer):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def add(self, uuid: UUID, name: Text, percent: float, color: BossBar_Color, style: BossBar_Style, darkenSky: bool, dragonMusic: bool, thickenFog: bool) -> None:
		pass

	@overload
	def remove(self, uuid: UUID) -> None:
		pass

	@overload
	def updateProgress(self, uuid: UUID, percent: float) -> None:
		pass

	@overload
	def updateName(self, uuid: UUID, name: Text) -> None:
		pass

	@overload
	def updateStyle(self, id: UUID, color: BossBar_Color, style: BossBar_Style) -> None:
		pass

	@overload
	def updateProperties(self, uuid: UUID, darkenSky: bool, dragonMusic: bool, thickenFog: bool) -> None:
		pass

	pass


