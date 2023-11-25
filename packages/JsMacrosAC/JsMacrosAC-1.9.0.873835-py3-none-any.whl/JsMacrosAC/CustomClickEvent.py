from typing import overload
from typing import TypeVar

net_minecraft_text_ClickEvent = TypeVar("net_minecraft_text_ClickEvent")
ClickEvent = net_minecraft_text_ClickEvent

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable


class CustomClickEvent(ClickEvent):

	@overload
	def __init__(self, event: Runnable) -> None:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def getEvent(self) -> Runnable:
		pass

	pass


