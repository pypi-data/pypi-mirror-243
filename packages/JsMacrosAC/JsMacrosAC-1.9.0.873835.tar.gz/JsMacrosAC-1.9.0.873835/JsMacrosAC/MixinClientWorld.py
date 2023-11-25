from typing import overload
from typing import TypeVar

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

net_minecraft_entity_Entity_RemovalReason = TypeVar("net_minecraft_entity_Entity_RemovalReason")
Entity_RemovalReason = net_minecraft_entity_Entity_RemovalReason

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo


class MixinClientWorld:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onAddEntity(self, entity: Entity, ci: CallbackInfo) -> None:
		pass

	@overload
	def onRemoveEntity(self, entityId: int, removalReason: Entity_RemovalReason, ci: CallbackInfo, entity: Entity) -> None:
		pass

	pass


