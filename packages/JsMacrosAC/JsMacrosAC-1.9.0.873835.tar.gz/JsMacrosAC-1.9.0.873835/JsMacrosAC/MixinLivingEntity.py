from typing import overload
from typing import TypeVar

net_minecraft_entity_EntityType__ = TypeVar("net_minecraft_entity_EntityType__")
EntityType = net_minecraft_entity_EntityType__

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_world_World = TypeVar("net_minecraft_world_World")
World = net_minecraft_world_World


class MixinLivingEntity(Entity):

	@overload
	def __init__(self, arg: EntityType, arg2: World) -> None:
		pass

	@overload
	def getMaxHealth(self) -> float:
		pass

	@overload
	def onSetHealth(self, health: float, ci: CallbackInfo) -> None:
		pass

	pass


