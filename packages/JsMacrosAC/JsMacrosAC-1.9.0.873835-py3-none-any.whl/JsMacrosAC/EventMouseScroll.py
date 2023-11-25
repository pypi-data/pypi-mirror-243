from typing import overload
from .BaseEvent import BaseEvent


class EventMouseScroll(BaseEvent):
	"""
	Since: 1.9.0 
	"""
	deltaX: float
	deltaY: float

	@overload
	def __init__(self, deltaX: float, deltaY: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


