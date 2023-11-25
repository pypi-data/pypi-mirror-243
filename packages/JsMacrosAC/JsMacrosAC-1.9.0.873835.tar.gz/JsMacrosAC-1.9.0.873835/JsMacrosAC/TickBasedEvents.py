from typing import overload
from typing import TypeVar

net_minecraft_client_MinecraftClient = TypeVar("net_minecraft_client_MinecraftClient")
MinecraftClient = net_minecraft_client_MinecraftClient

net_minecraft_client_network_MultiplayerServerListPinger = TypeVar("net_minecraft_client_network_MultiplayerServerListPinger")
MultiplayerServerListPinger = net_minecraft_client_network_MultiplayerServerListPinger

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class TickBasedEvents:
	serverListPinger: MultiplayerServerListPinger

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def areNotEqual(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def areTagsEqualIgnoreDamage(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def areEqualIgnoreDamage(self, a: ItemStack, b: ItemStack) -> bool:
		pass

	@overload
	def onTick(self, mc: MinecraftClient) -> None:
		pass

	pass


