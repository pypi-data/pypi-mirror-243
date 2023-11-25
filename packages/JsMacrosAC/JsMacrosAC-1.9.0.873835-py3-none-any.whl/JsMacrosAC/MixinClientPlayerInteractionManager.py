from typing import overload
from typing import TypeVar

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_net_minecraft_util_ActionResult_ = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_net_minecraft_util_ActionResult_")
CallbackInfoReturnable = org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_net_minecraft_util_ActionResult_

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos

net_minecraft_client_network_ClientPlayerEntity = TypeVar("net_minecraft_client_network_ClientPlayerEntity")
ClientPlayerEntity = net_minecraft_client_network_ClientPlayerEntity

net_minecraft_util_hit_BlockHitResult = TypeVar("net_minecraft_util_hit_BlockHitResult")
BlockHitResult = net_minecraft_util_hit_BlockHitResult

net_minecraft_util_Hand = TypeVar("net_minecraft_util_Hand")
Hand = net_minecraft_util_Hand

net_minecraft_util_math_Direction = TypeVar("net_minecraft_util_math_Direction")
Direction = net_minecraft_util_math_Direction

net_minecraft_entity_player_PlayerEntity = TypeVar("net_minecraft_entity_player_PlayerEntity")
PlayerEntity = net_minecraft_entity_player_PlayerEntity


class MixinClientPlayerInteractionManager:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onInteractBlock(self, player: ClientPlayerEntity, hand: Hand, hitResult: BlockHitResult, cir: CallbackInfoReturnable) -> None:
		pass

	@overload
	def onAttackBlock(self, pos: BlockPos, direction: Direction, cir: CallbackInfoReturnable) -> None:
		pass

	@overload
	def onAttackEntity(self, player: PlayerEntity, target: Entity, ci: CallbackInfo) -> None:
		pass

	@overload
	def onInteractEntity(self, player: PlayerEntity, entity: Entity, hand: Hand, cir: CallbackInfoReturnable) -> None:
		pass

	pass


