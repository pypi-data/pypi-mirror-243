from typing import overload
from typing import TypeVar

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack

net_minecraft_screen_PropertyDelegate = TypeVar("net_minecraft_screen_PropertyDelegate")
PropertyDelegate = net_minecraft_screen_PropertyDelegate


class MixinAbstractFurnaceScreenHandler:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeIsSmeltable(self, itemStack: ItemStack) -> bool:
		pass

	@overload
	def invokeIsFuel(self, itemStack: ItemStack) -> bool:
		pass

	@overload
	def getPropertyDelegate(self) -> PropertyDelegate:
		pass

	pass


