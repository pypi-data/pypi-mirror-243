from typing import overload
from typing import List
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper
from .AbstractHorseEntityHelper import AbstractHorseEntityHelper


class HorseInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def canBeSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the horse can be saddled, 'false' otherwise. 
		"""
		pass

	@overload
	def isSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the horse is saddled, 'false' otherwise. 
		"""
		pass

	@overload
	def getSaddle(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the saddle item. 
		"""
		pass

	@overload
	def hasArmorSlot(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the horse can equip armor, 'false' otherwise. 
		"""
		pass

	@overload
	def getArmor(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the armor item. 
		"""
		pass

	@overload
	def hasChest(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the horse has equipped a chest, 'false' otherwise. 
		"""
		pass

	@overload
	def getInventorySize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the horse's inventory size. 
		"""
		pass

	@overload
	def getHorseInventory(self) -> List[ItemStackHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of items in the horse's inventory. 
		"""
		pass

	@overload
	def getHorse(self) -> AbstractHorseEntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the horse this inventory belongs to. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


