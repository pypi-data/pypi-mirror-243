from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

net_minecraft_entity_effect_StatusEffect = TypeVar("net_minecraft_entity_effect_StatusEffect")
StatusEffect = net_minecraft_entity_effect_StatusEffect

net_minecraft_entity_effect_StatusEffectInstance = TypeVar("net_minecraft_entity_effect_StatusEffectInstance")
StatusEffectInstance = net_minecraft_entity_effect_StatusEffectInstance


class StatusEffectHelper(BaseHelper):
	"""
	Since: 1.2.4 
	"""

	@overload
	def __init__(self, s: StatusEffectInstance) -> None:
		pass

	@overload
	def __init__(self, s: StatusEffect) -> None:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def __init__(self, s: StatusEffect, t: int) -> None:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.2.4 
		"""
		pass

	@overload
	def getStrength(self) -> int:
		"""
		Since: 1.2.4 
		"""
		pass

	@overload
	def getCategory(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the string name of the category of the status effect, "HARMFUL", "NEUTRAL", or "BENEFICIAL". 
		"""
		pass

	@overload
	def getTime(self) -> int:
		"""
		Since: 1.2.4 
		"""
		pass

	@overload
	def isPermanent(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect is applied permanently, 'false' otherwise. 
		"""
		pass

	@overload
	def isAmbient(self) -> bool:
		"""Ambient effects are usually applied through beacons and they make the particles more
translucent.\n
		Since: 1.8.4 

		Returns:
			'true' if this effect is an ambient one, 'false' otherwise. 
		"""
		pass

	@overload
	def hasIcon(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect has an icon it should render, 'false' otherwise. 
		"""
		pass

	@overload
	def isVisible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect affects the particle color and gets rendered in game, 'false' otherwise. 
		"""
		pass

	@overload
	def isInstant(self) -> bool:
		"""An effect which is instant can still have a duration, but only if it's set through a
command.\n
		Since: 1.8.4 

		Returns:
			'true' if this effect should be applied instantly, 'false' otherwise. 
		"""
		pass

	@overload
	def isBeneficial(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect is considered beneficial, 'false' otherwise. 
		"""
		pass

	@overload
	def isNeutral(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect is considered neutral, 'false' otherwise. 
		"""
		pass

	@overload
	def isHarmful(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this effect is considered harmful, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


