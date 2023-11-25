from typing import overload
from typing import TypeVar

net_minecraft_network_packet_s2c_play_ScreenHandlerSlotUpdateS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_ScreenHandlerSlotUpdateS2CPacket")
ScreenHandlerSlotUpdateS2CPacket = net_minecraft_network_packet_s2c_play_ScreenHandlerSlotUpdateS2CPacket

net_minecraft_network_packet_s2c_play_BlockUpdateS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_BlockUpdateS2CPacket")
BlockUpdateS2CPacket = net_minecraft_network_packet_s2c_play_BlockUpdateS2CPacket

net_minecraft_network_packet_s2c_play_BlockEntityUpdateS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_BlockEntityUpdateS2CPacket")
BlockEntityUpdateS2CPacket = net_minecraft_network_packet_s2c_play_BlockEntityUpdateS2CPacket

net_minecraft_network_packet_s2c_play_PlayerListS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_PlayerListS2CPacket")
PlayerListS2CPacket = net_minecraft_network_packet_s2c_play_PlayerListS2CPacket

net_minecraft_network_packet_s2c_play_PlayerRemoveS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_PlayerRemoveS2CPacket")
PlayerRemoveS2CPacket = net_minecraft_network_packet_s2c_play_PlayerRemoveS2CPacket

net_minecraft_client_network_ClientCommonNetworkHandler = TypeVar("net_minecraft_client_network_ClientCommonNetworkHandler")
ClientCommonNetworkHandler = net_minecraft_client_network_ClientCommonNetworkHandler

net_minecraft_network_packet_s2c_play_ChunkDataS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_ChunkDataS2CPacket")
ChunkDataS2CPacket = net_minecraft_network_packet_s2c_play_ChunkDataS2CPacket

net_minecraft_network_packet_s2c_play_InventoryS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_InventoryS2CPacket")
InventoryS2CPacket = net_minecraft_network_packet_s2c_play_InventoryS2CPacket

net_minecraft_client_network_PlayerListEntry = TypeVar("net_minecraft_client_network_PlayerListEntry")
PlayerListEntry = net_minecraft_client_network_PlayerListEntry

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_network_packet_s2c_play_ItemPickupAnimationS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_ItemPickupAnimationS2CPacket")
ItemPickupAnimationS2CPacket = net_minecraft_network_packet_s2c_play_ItemPickupAnimationS2CPacket

net_minecraft_network_packet_s2c_play_EntityStatusEffectS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_EntityStatusEffectS2CPacket")
EntityStatusEffectS2CPacket = net_minecraft_network_packet_s2c_play_EntityStatusEffectS2CPacket

net_minecraft_network_packet_s2c_play_PlayerListS2CPacket_Entry = TypeVar("net_minecraft_network_packet_s2c_play_PlayerListS2CPacket_Entry")
PlayerListS2CPacket_Entry = net_minecraft_network_packet_s2c_play_PlayerListS2CPacket_Entry

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_network_packet_s2c_play_GameJoinS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_GameJoinS2CPacket")
GameJoinS2CPacket = net_minecraft_network_packet_s2c_play_GameJoinS2CPacket

net_minecraft_network_packet_s2c_play_RemoveEntityStatusEffectS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_RemoveEntityStatusEffectS2CPacket")
RemoveEntityStatusEffectS2CPacket = net_minecraft_network_packet_s2c_play_RemoveEntityStatusEffectS2CPacket

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID

net_minecraft_network_packet_s2c_play_UnloadChunkS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_UnloadChunkS2CPacket")
UnloadChunkS2CPacket = net_minecraft_network_packet_s2c_play_UnloadChunkS2CPacket

net_minecraft_network_packet_s2c_play_ChunkDeltaUpdateS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_ChunkDeltaUpdateS2CPacket")
ChunkDeltaUpdateS2CPacket = net_minecraft_network_packet_s2c_play_ChunkDeltaUpdateS2CPacket

net_minecraft_network_packet_s2c_play_BossBarS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_BossBarS2CPacket")
BossBarS2CPacket = net_minecraft_network_packet_s2c_play_BossBarS2CPacket


class MixinClientPlayNetworkHandler(ClientCommonNetworkHandler):

	@overload
	def onPlayerList(self, packet: PlayerListS2CPacket, ci: CallbackInfo, var2: iter, entry: PlayerListS2CPacket_Entry, playerListEntry: PlayerListEntry) -> None:
		pass

	@overload
	def onPlayerListEnd(self, packet: PlayerRemoveS2CPacket, ci: CallbackInfo, var2: iter, uUID: UUID, playerListEntry: PlayerListEntry) -> None:
		pass

	@overload
	def onTitle(self, title: Text) -> Text:
		pass

	@overload
	def onSubtitle(self, title: Text) -> Text:
		pass

	@overload
	def onBossBar(self, packet: BossBarS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onItemPickupAnimation(self, packet: ItemPickupAnimationS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onGameJoin(self, packet: GameJoinS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onChunkData(self, packet: ChunkDataS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onBlockUpdate(self, packet: BlockUpdateS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onChunkDeltaUpdate(self, packet: ChunkDeltaUpdateS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onBlockEntityUpdate(self, packet: BlockEntityUpdateS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onUnloadChunk(self, packet: UnloadChunkS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onEntityStatusEffect(self, packet: EntityStatusEffectS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onEntityStatusEffect(self, packet: RemoveEntityStatusEffectS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onHeldSlotUpdate(self, packet: ScreenHandlerSlotUpdateS2CPacket, ci: CallbackInfo) -> None:
		pass

	@overload
	def onInventorySlotUpdate(self, packet: ScreenHandlerSlotUpdateS2CPacket, ci: CallbackInfo) -> None:
		pass

	@overload
	def onScreenSlotUpdate(self, packet: ScreenHandlerSlotUpdateS2CPacket, ci: CallbackInfo) -> None:
		pass

	@overload
	def onScreenSlotUpdate2(self, packet: ScreenHandlerSlotUpdateS2CPacket, ci: CallbackInfo) -> None:
		pass

	@overload
	def onInventoryUpdate(self, packet: InventoryS2CPacket, ci: CallbackInfo) -> None:
		pass

	pass


