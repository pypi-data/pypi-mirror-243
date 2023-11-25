from typing import overload
from .BaseEvent import BaseEvent


class EventQuitGame(BaseEvent):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


