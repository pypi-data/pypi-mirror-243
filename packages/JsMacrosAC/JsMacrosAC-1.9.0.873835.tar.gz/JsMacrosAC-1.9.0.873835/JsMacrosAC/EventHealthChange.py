from typing import overload
from .BaseEvent import BaseEvent


class EventHealthChange(BaseEvent):
	"""
	Since: 1.8.4 
	"""
	health: float
	change: float

	@overload
	def __init__(self, health: float, change: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


