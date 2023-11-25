from typing import overload
from .BaseEvent import BaseEvent


class EventLaunchGame(BaseEvent):
	"""
	Since: 1.8.4 
	"""
	playerName: str

	@overload
	def __init__(self, playerName: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


