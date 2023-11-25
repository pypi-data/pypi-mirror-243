from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper
from .ItemStackHelper import ItemStackHelper

net_minecraft_entity_ItemEntity = TypeVar("net_minecraft_entity_ItemEntity")
ItemEntity = net_minecraft_entity_ItemEntity


class ItemEntityHelper(EntityHelper):

	@overload
	def __init__(self, e: ItemEntity) -> None:
		pass

	@overload
	def getContainedItemStack(self) -> ItemStackHelper:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


