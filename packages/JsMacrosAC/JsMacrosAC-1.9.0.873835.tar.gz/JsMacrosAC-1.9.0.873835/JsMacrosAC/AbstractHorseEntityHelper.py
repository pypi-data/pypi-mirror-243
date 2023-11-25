from typing import overload
from typing import TypeVar
from typing import Generic
from .AnimalEntityHelper import AnimalEntityHelper

T = TypeVar("T")

class AbstractHorseEntityHelper(Generic[T], AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def getOwner(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the UUID of this horse's owner, or 'null' if it has no owner. 
		"""
		pass

	@overload
	def isTame(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse is already tamed, 'false' otherwise. 
		"""
		pass

	@overload
	def isSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse is saddled, 'false' otherwise. 
		"""
		pass

	@overload
	def isAngry(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse is angry, 'false' otherwise. 
		"""
		pass

	@overload
	def isBred(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse was bred and not naturally spawned, 'false' otherwise. 
		"""
		pass

	@overload
	def isEating(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse is currently eating, 'false' otherwise. 
		"""
		pass

	@overload
	def canWearArmor(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse can wear armor, 'false' otherwise. 
		"""
		pass

	@overload
	def canBeSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this horse can be saddled, 'false' otherwise. 
		"""
		pass

	@overload
	def getInventorySize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			this horse's inventory size. 
		"""
		pass

	@overload
	def getJumpStrengthStat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			this horse's jump strength. 
		"""
		pass

	@overload
	def getHorseJumpHeight(self) -> float:
		"""The result of this method is only an approximation, but it's really close.\n
		Since: 1.8.4 

		Returns:
			this horse's maximum jump height for its current jump strength. 
		"""
		pass

	@overload
	def getMaxJumpStrengthStat(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum possible value of a horse's jump strength. 
		"""
		pass

	@overload
	def getMinJumpStrengthStat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the minimum possible value of a horse's jump strength. 
		"""
		pass

	@overload
	def getSpeedStat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			this horse's speed stat. 
		"""
		pass

	@overload
	def getHorseSpeed(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			this horse's speed in blocks per second. 
		"""
		pass

	@overload
	def getMaxSpeedStat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the maximum possible value of a horse's speed stat. 
		"""
		pass

	@overload
	def getMinSpeedStat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the minimum possible value of a horse's speed stat. 
		"""
		pass

	@overload
	def getHealthStat(self) -> float:
		"""The returned value is equal to LivingEntityHelper#getMaxHealth() .\n
		Since: 1.8.4 

		Returns:
			this horse's health stat. 
		"""
		pass

	@overload
	def getMaxHealthStat(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum possible value of a horse's health stat. 
		"""
		pass

	@overload
	def getMinHealthStat(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the minimum possible value of a horse's health stat. 
		"""
		pass

	pass


