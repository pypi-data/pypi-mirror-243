from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .ItemStackHelper import ItemStackHelper
from .Pos2D import Pos2D

T = TypeVar("T")
net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class Inventory(Generic[T]):
	"""
	Since: 1.0.8 
	"""

	@overload
	def create(self) -> "Inventory":
		pass

	@overload
	def create(self, s: Screen) -> "Inventory":
		pass

	@overload
	def click(self, slot: int) -> "Inventory":
		"""
		Since: 1.5.0 

		Args:
			slot: 
		"""
		pass

	@overload
	def click(self, slot: int, mousebutton: int) -> "Inventory":
		"""Clicks a slot with a mouse button.~~if the slot is a container, it will click the first slot in the container\n
		Since: 1.0.8 

		Args:
			mousebutton: 
			slot: 
		"""
		pass

	@overload
	def dragClick(self, slots: List[int], mousebutton: int) -> "Inventory":
		"""Does a drag-click with a mouse button. (the slots don't have to be in order or even adjacent, but when vanilla minecraft calls the underlying function they're always sorted...)

		Args:
			slots: 
			mousebutton: 
		"""
		pass

	@overload
	def dropSlot(self, slot: int) -> "Inventory":
		"""
		Since: 1.5.0 

		Args:
			slot: 
		"""
		pass

	@overload
	def dropSlot(self, slot: int, stack: bool) -> "Inventory":
		"""
		Since: 1.8.4 

		Args:
			stack: decide whether to drop the whole stack or just a single item 
			slot: the slot to drop 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def contains(self, item: ItemStackHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check for 

		Returns:
			'true' if the item is contined anywhere in the inventory, 'false' otherwise. 
		"""
		pass

	@overload
	def contains(self, item: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			item: the item to check for 

		Returns:
			'true' if the item is contined anywhere in the inventory, 'false' otherwise. 
		"""
		pass

	@overload
	def findFreeInventorySlot(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first empty slot in the main inventory or '-1' if there are no empty
slots. 
		"""
		pass

	@overload
	def findFreeHotbarSlot(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first empty hotbar slot or '-1' if there are no empty slots. 
		"""
		pass

	@overload
	def findFreeSlot(self, mapIdentifiers: List[str]) -> int:
		"""
		Since: 1.8.4 

		Args:
			mapIdentifiers: the identifier of the inventory sections to check 

		Returns:
			the first empty slot in the given inventory sections, or '-1' if there are no
empty slots. 
		"""
		pass

	@overload
	def getItemCount(self) -> Mapping[str, int]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all item ids and their total count inside the inventory. 
		"""
		pass

	@overload
	def getItems(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all items in the inventory. 
		"""
		pass

	@overload
	def getItems(self, mapIdentifiers: List[str]) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Args:
			mapIdentifiers: the inventory sections 

		Returns:
			a list of all items in the given inventory sections. 
		"""
		pass

	@overload
	def findItem(self, item: ItemStackHelper) -> List[int]:
		"""
		Since: 1.8.4 

		Args:
			item: the item to search for 

		Returns:
			all slots containing the given item. 
		"""
		pass

	@overload
	def findItem(self, item: str) -> List[int]:
		"""
		Since: 1.8.4 

		Args:
			item: the item to search for 

		Returns:
			all slots containing the given item. 
		"""
		pass

	@overload
	def getSlots(self, mapIdentifiers: List[str]) -> List[int]:
		"""
		Since: 1.8.4 

		Args:
			mapIdentifiers: the inventory sections 

		Returns:
			all slots indexes in the given inventory sections. 
		"""
		pass

	@overload
	def getSelectedHotbarSlotIndex(self) -> int:
		"""
		Since: 1.2.5 

		Returns:
			the index of the selected hotbar slot. 
		"""
		pass

	@overload
	def setSelectedHotbarSlotIndex(self, index: int) -> None:
		"""
		Since: 1.2.5 

		Args:
			index: 
		"""
		pass

	@overload
	def closeAndDrop(self) -> "Inventory":
		"""closes the inventory, (if the inventory/container is visible it will close the gui). also drops any "held on mouse" items.
		"""
		pass

	@overload
	def close(self) -> None:
		"""Closes the inventory, and open gui if applicable.
		"""
		pass

	@overload
	def quick(self, slot: int) -> "Inventory":
		"""simulates a shift-click on a slot.
It should be safe to chain these without FClient#waitTick() at least for a bunch of the same item.

		Args:
			slot: 
		"""
		pass

	@overload
	def quickAll(self, slot: int) -> int:
		"""
		Since: 1.7.0 

		Args:
			slot: 
		"""
		pass

	@overload
	def quickAll(self, slot: int, button: int) -> int:
		"""quicks all that match the slot\n
		Since: 1.7.0 

		Args:
			button: 
			slot: a slot from the section you want to move items from 

		Returns:
			number of items that matched 
		"""
		pass

	@overload
	def getHeld(self) -> ItemStackHelper:
		"""

		Returns:
			the held (by the mouse) item. 
		"""
		pass

	@overload
	def getSlot(self, slot: int) -> ItemStackHelper:
		"""

		Args:
			slot: 

		Returns:
			the item in the slot. 
		"""
		pass

	@overload
	def getTotalSlots(self) -> int:
		"""

		Returns:
			the size of the container/inventory. 
		"""
		pass

	@overload
	def split(self, slot1: int, slot2: int) -> "Inventory":
		"""Splits the held stack into two slots. can be alternatively done with Inventory#dragClick(int[],int) if this one has issues on some servers.

		Args:
			slot2: 
			slot1: 
		"""
		pass

	@overload
	def grabAll(self, slot: int) -> "Inventory":
		"""Does that double click thingy to turn a incomplete stack pickup into a complete stack pickup if you have more in your inventory.

		Args:
			slot: 
		"""
		pass

	@overload
	def swap(self, slot1: int, slot2: int) -> "Inventory":
		"""swaps the items in two slots.

		Args:
			slot2: 
			slot1: 
		"""
		pass

	@overload
	def swapHotbar(self, slot: int, hotbarSlot: int) -> "Inventory":
		"""equivalent to hitting the numbers or f for swapping slots to hotbar\n
		Since: 1.6.5 [citation needed] 

		Args:
			hotbarSlot: 0-8 or 40 for offhand 
			slot: 
		"""
		pass

	@overload
	def openGui(self) -> None:
		"""
		Since: 1.2.8 
		"""
		pass

	@overload
	def getSlotUnderMouse(self) -> int:
		"""
		Since: 1.1.3 

		Returns:
			the id of the slot under the mouse. 
		"""
		pass

	@overload
	def getType(self) -> str:
		"""
		Since: 1.1.3 

		Returns:
			the part of the mapping the slot is in. 
		"""
		pass

	@overload
	def getMap(self) -> Mapping[str, List[int]]:
		"""
		Since: 1.1.3 

		Returns:
			the inventory mappings different depending on the type of open container/inventory. 
		"""
		pass

	@overload
	def getLocation(self, slotNum: int) -> str:
		"""
		Since: 1.1.3 

		Args:
			slotNum: 

		Returns:
			returns the part of the mapping the slot is in. 
		"""
		pass

	@overload
	def getSlotPos(self, slot: int) -> Pos2D:
		"""
		Since: 1.8.4 

		Returns:
			the x/y position of the specified slot index 
		"""
		pass

	@overload
	def isContainer(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the inventory is a container, 'false' otherwise. 
		"""
		pass

	@overload
	def getContainerTitle(self) -> str:
		"""
		Since: 1.2.3 
		"""
		pass

	@overload
	def getRawContainer(self) -> T:
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def getCurrentSyncId(self) -> int:
		"""
		Since: 1.6.0 
		"""
		pass

	pass


