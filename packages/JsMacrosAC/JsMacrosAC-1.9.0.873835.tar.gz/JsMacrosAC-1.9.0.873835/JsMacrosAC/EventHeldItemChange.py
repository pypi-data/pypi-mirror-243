from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ItemStackHelper import ItemStackHelper

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class EventHeldItemChange(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	offHand: bool
	item: ItemStackHelper
	oldItem: ItemStackHelper

	@overload
	def __init__(self, item: ItemStack, oldItem: ItemStack, offHand: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


