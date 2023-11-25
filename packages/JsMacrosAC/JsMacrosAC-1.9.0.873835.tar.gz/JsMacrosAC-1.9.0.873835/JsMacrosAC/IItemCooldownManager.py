from typing import overload
from typing import TypeVar
from typing import Mapping
from .IItemCooldownEntry import IItemCooldownEntry

net_minecraft_item_Item = TypeVar("net_minecraft_item_Item")
Item = net_minecraft_item_Item


class IItemCooldownManager:

	@overload
	def jsmacros_getCooldownItems(self) -> Mapping[Item, IItemCooldownEntry]:
		pass

	@overload
	def jsmacros_getManagerTicks(self) -> int:
		pass

	pass


