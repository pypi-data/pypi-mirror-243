from typing import overload
from typing import TypeVar

net_minecraft_screen_slot_Slot = TypeVar("net_minecraft_screen_slot_Slot")
Slot = net_minecraft_screen_slot_Slot


class IInventory:

	@overload
	def jsmacros$getX(self) -> int:
		pass

	@overload
	def jsmacros$getY(self) -> int:
		pass

	@overload
	def jsmacros_getSlotUnder(self, x: float, y: float) -> Slot:
		pass

	pass


