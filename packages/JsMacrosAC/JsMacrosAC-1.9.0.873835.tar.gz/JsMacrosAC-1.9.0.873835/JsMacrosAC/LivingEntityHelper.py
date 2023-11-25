from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .EntityHelper import EntityHelper
from .StatusEffectHelper import StatusEffectHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")

class LivingEntityHelper(Generic[T], EntityHelper):

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getStatusEffects(self) -> List[StatusEffectHelper]:
		"""
		Since: 1.2.7 

		Returns:
			entity status effects. 
		"""
		pass

	@overload
	def canHaveStatusEffect(self, effect: StatusEffectHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			effect: the status effect 

		Returns:
			if the entity can have a certain status effect 
		"""
		pass

	@overload
	def hasStatusEffect(self, id: str) -> bool:
		"""For client side entities, excluding the player, this will most likely return 'false' even if the entity has the effect, as effects are not synced to the client.\n
		Since: 1.8.4 

		Returns:
			'true' if the entity has the specified status effect, 'false' otherwise. 
		"""
		pass

	@overload
	def isHolding(self, item: str) -> bool:
		"""
		Since: 1.9.0 

		Returns:
			'true' if the entity is holding the specified item 
		"""
		pass

	@overload
	def getMainHand(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's main hand. 
		"""
		pass

	@overload
	def getOffHand(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's off hand. 
		"""
		pass

	@overload
	def getHeadArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's head armor slot. 
		"""
		pass

	@overload
	def getChestArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's chest armor slot. 
		"""
		pass

	@overload
	def getLegArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's leg armor slot. 
		"""
		pass

	@overload
	def getFootArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.7 

		Returns:
			the item in the entity's foot armor slot. 
		"""
		pass

	@overload
	def getHealth(self) -> float:
		"""
		Since: 1.3.1 

		Returns:
			entity's health 
		"""
		pass

	@overload
	def getMaxHealth(self) -> float:
		"""
		Since: 1.6.5 

		Returns:
			entity's max health 
		"""
		pass

	@overload
	def getAbsorptionHealth(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the entity's absorption amount. 
		"""
		pass

	@overload
	def getArmor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the entity's armor value. 
		"""
		pass

	@overload
	def getDefaultHealth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the entity's default health. 
		"""
		pass

	@overload
	def getMobCategory(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the entity's mob category, 'UNDEAD' , 'DEFAULT' , 'ARTHROPOD' , or 'ILLAGER' , 'AQUATIC' or 'UNKNOWN' . 
		"""
		pass

	@overload
	def isSleeping(self) -> bool:
		"""
		Since: 1.2.7 

		Returns:
			if the entity is in a bed. 
		"""
		pass

	@overload
	def isFallFlying(self) -> bool:
		"""
		Since: 1.5.0 

		Returns:
			if the entity has elytra deployed 
		"""
		pass

	@overload
	def isOnGround(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity is on the ground 
		"""
		pass

	@overload
	def canBreatheInWater(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity can breathe in water 
		"""
		pass

	@overload
	def hasNoDrag(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity has no drag 
		"""
		pass

	@overload
	def hasNoGravity(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity has no gravity 
		"""
		pass

	@overload
	def canTarget(self, target: "LivingEntityHelper") -> bool:
		"""
		Since: 1.8.4 

		Args:
			target: the target entity 

		Returns:
			if the entity can target a target entity 
		"""
		pass

	@overload
	def canTakeDamage(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity can take damage 
		"""
		pass

	@overload
	def isPartOfGame(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity is part of the game (is alive and not spectator) 
		"""
		pass

	@overload
	def isSpectator(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity is in spectator 
		"""
		pass

	@overload
	def isUndead(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			if the entity is undead 
		"""
		pass

	@overload
	def getBowPullProgress(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the bow pull progress of the entity, '0' by default. 
		"""
		pass

	@overload
	def getItemUseTimeLeft(self) -> int:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def isBaby(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is a baby, 'false' otherwise. 
		"""
		pass

	@overload
	def canSeeEntity(self, entity: EntityHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			entity: the entity to check line of sight to 

		Returns:
			'true' if the player has line of sight to the specified entity, 'false' otherwise. 
		"""
		pass

	@overload
	def canSeeEntity(self, entity: EntityHelper, simpleCast: bool) -> bool:
		"""
		Since: 1.8.4 

		Args:
			simpleCast: whether to use a simple raycast or a more complex one 
			entity: the entity to check line of sight to 

		Returns:
			'true' if the entity has line of sight to the specified entity, 'false' otherwise. 
		"""
		pass

	pass


