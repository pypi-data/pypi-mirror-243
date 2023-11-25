from typing import overload
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .StatusEffectHelper import StatusEffectHelper

net_minecraft_item_FoodComponent = TypeVar("net_minecraft_item_FoodComponent")
FoodComponent = net_minecraft_item_FoodComponent


class FoodComponentHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FoodComponent) -> None:
		pass

	@overload
	def getHunger(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of hunger this food restores. 
		"""
		pass

	@overload
	def getSaturation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the amount of saturation this food restores. 
		"""
		pass

	@overload
	def isMeat(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this food can be eaten by wolves, 'false' otherwise. 
		"""
		pass

	@overload
	def isAlwaysEdible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this food can be eaten even when the player is not hungry, 'false' otherwise. 
		"""
		pass

	@overload
	def isFastFood(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the food can be eaten faster than usual, 'false' otherwise. 
		"""
		pass

	@overload
	def getStatusEffects(self) -> Mapping[StatusEffectHelper, Float]:
		"""
		Since: 1.8.4 

		Returns:
			a map of status effects and their respective probabilities. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


