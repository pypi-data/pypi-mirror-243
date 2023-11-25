from typing import overload
from .BaseEvent import BaseEvent
from .StatusEffectHelper import StatusEffectHelper


class EventStatusEffectUpdate(BaseEvent):
	"""
	Since: 1.8.4 
	"""
	oldEffect: StatusEffectHelper
	newEffect: StatusEffectHelper
	added: bool
	removed: bool

	@overload
	def __init__(self, oldEffect: StatusEffectHelper, newEffect: StatusEffectHelper, added: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


