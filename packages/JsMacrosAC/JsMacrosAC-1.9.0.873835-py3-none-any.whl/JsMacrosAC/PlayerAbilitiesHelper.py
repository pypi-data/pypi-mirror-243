from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

net_minecraft_entity_player_PlayerAbilities = TypeVar("net_minecraft_entity_player_PlayerAbilities")
PlayerAbilities = net_minecraft_entity_player_PlayerAbilities


class PlayerAbilitiesHelper(BaseHelper):
	"""
	Since: 1.0.3 
	"""

	@overload
	def __init__(self, a: PlayerAbilities) -> None:
		pass

	@overload
	def getInvulnerable(self) -> bool:
		"""
		Since: 1.0.3 

		Returns:
			whether the player can be damaged. 
		"""
		pass

	@overload
	def getFlying(self) -> bool:
		"""
		Since: 1.0.3 

		Returns:
			if the player is currently flying. 
		"""
		pass

	@overload
	def getAllowFlying(self) -> bool:
		"""
		Since: 1.0.3 

		Returns:
			if the player is allowed to fly. 
		"""
		pass

	@overload
	def getCreativeMode(self) -> bool:
		"""
		Since: 1.0.3 

		Returns:
			if the player is in creative. 
		"""
		pass

	@overload
	def canModifyWorld(self) -> bool:
		"""Even if this method returns true, the player may not be able to modify the world due to other
restrictions such as plugins and mods. Modifying the world includes, placing, breaking or
interacting with blocks.\n
		Since: 1.8.4 

		Returns:
			'true' if the player is allowed to modify the world, 'false' otherwise. 
		"""
		pass

	@overload
	def setFlying(self, b: bool) -> "PlayerAbilitiesHelper":
		"""set the player flying state.\n
		Since: 1.0.3 

		Args:
			b: 
		"""
		pass

	@overload
	def setAllowFlying(self, b: bool) -> "PlayerAbilitiesHelper":
		"""set the player allow flying state.\n
		Since: 1.0.3 

		Args:
			b: 
		"""
		pass

	@overload
	def getFlySpeed(self) -> float:
		"""
		Since: 1.0.3 

		Returns:
			the player fly speed multiplier. 
		"""
		pass

	@overload
	def setFlySpeed(self, flySpeed: float) -> "PlayerAbilitiesHelper":
		"""set the player fly speed multiplier.\n
		Since: 1.0.3 

		Args:
			flySpeed: 
		"""
		pass

	@overload
	def getWalkSpeed(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the player's walk speed. 
		"""
		pass

	@overload
	def setWalkSpeed(self, speed: float) -> "PlayerAbilitiesHelper":
		"""
		Since: 1.8.4 

		Args:
			speed: the new walk speed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


