from typing import overload
from typing import List
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper
from .TextHelper import TextHelper


class CreativeInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def scroll(self, amount: float) -> "CreativeInventory":
		"""The total scroll value is always clamp between 0 and 1.\n
		Since: 1.8.4 

		Args:
			amount: the amount to scroll by, between -1 and 1 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def scrollTo(self, position: float) -> "CreativeInventory":
		"""The total scroll value is always clamp between 0 and 1.\n
		Since: 1.8.4 

		Args:
			position: the position to scroll to, between 0 and 1 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getShownItems(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all shown items. 
		"""
		pass

	@overload
	def search(self, search: str) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			search: the string to search for 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def selectSearch(self) -> "CreativeInventory":
		"""Select the search tab.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def selectInventory(self) -> "CreativeInventory":
		"""Select the inventory tab.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def selectHotbar(self) -> "CreativeInventory":
		"""Select the tab where the hotbars are stored.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def selectTab(self, tabName: str) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			tabName: the name of the tab to select 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTabNames(self) -> List[str]:
		pass

	@overload
	def getTabTexts(self) -> List[TextHelper]:
		pass

	@overload
	def destroyHeldItem(self) -> "CreativeInventory":
		"""Destroys the currently held item.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def destroyAllItems(self) -> "CreativeInventory":
		"""Destroys all items in the player's inventory.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setCursorStack(self, stack: ItemStackHelper) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			stack: the item stack to drag 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setStack(self, slot: int, stack: ItemStackHelper) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			stack: the item stack to insert 
			slot: the slot to insert the item into 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def saveHotbar(self, index: int) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			index: the index to save the hotbar to, from 0 to 8 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def restoreHotbar(self, index: int) -> "CreativeInventory":
		"""
		Since: 1.8.4 

		Args:
			index: the index to save the hotbar to, from 0 to 8 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSavedHotbar(self, index: int) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Args:
			index: the index to save the hotbar to, from 0 to 8 

		Returns:
			a list of all items in the saved hotbar. 
		"""
		pass

	@overload
	def isInHotbar(self, slot: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			slot: the slot to check 

		Returns:
			'true' if the slot is in the hotbar or the offhand slot, 'false' otherwise. 
		"""
		pass

	@overload
	def getOffhand(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item in the offhand. 
		"""
		pass

	@overload
	def getHelmet(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped helmet item. 
		"""
		pass

	@overload
	def getChestplate(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped chestplate item. 
		"""
		pass

	@overload
	def getLeggings(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped leggings item. 
		"""
		pass

	@overload
	def getBoots(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the equipped boots item. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


