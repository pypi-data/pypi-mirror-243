from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .TextHelper import TextHelper

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class EventTitle(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	type: str
	message: TextHelper

	@overload
	def __init__(self, type: str, message: Text) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


