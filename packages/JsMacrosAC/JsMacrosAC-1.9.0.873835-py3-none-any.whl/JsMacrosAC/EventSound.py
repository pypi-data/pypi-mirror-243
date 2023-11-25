from typing import overload
from .BaseEvent import BaseEvent
from .Pos3D import Pos3D


class EventSound(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	sound: str
	volume: float
	pitch: float
	position: Pos3D

	@overload
	def __init__(self, sound: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


