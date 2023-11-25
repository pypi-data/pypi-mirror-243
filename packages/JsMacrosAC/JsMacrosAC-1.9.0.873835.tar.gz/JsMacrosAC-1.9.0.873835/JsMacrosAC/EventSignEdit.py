from typing import overload
from typing import List
from .BaseEvent import BaseEvent
from .Pos3D import Pos3D


class EventSignEdit(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	pos: Pos3D
	closeScreen: bool
	signText: List[str]

	@overload
	def __init__(self, signText: List[str], x: int, y: int, z: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


