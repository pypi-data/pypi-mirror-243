from typing import overload
from typing import TypeVar

net_minecraft_screen_slot_SlotActionType = TypeVar("net_minecraft_screen_slot_SlotActionType")
SlotActionType = net_minecraft_screen_slot_SlotActionType

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_screen_slot_Slot = TypeVar("net_minecraft_screen_slot_Slot")
Slot = net_minecraft_screen_slot_Slot


class MixinHandledScreen:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def beforeMouseClick(self, slot: Slot, slotId: int, button: int, actionType: SlotActionType, ci: CallbackInfo) -> None:
		pass

	pass


