from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ItemStackHelper import ItemStackHelper

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class EventItemDamage(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	item: ItemStackHelper
	damage: int

	@overload
	def __init__(self, stack: ItemStack, damage: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


