from typing import overload
from typing import List
from .BaseEvent import BaseEvent
from .BlockPosHelper import BlockPosHelper
from .ItemStackHelper import ItemStackHelper


class EventDeath(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	deathPos: BlockPosHelper
	inventory: List[ItemStackHelper]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def respawn(self) -> None:
		"""Respawns the player. Should be used with some delay, one tick should be enough.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


