from typing import overload
from typing import TypeVar
from .IPlayerListHud import IPlayerListHud

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class MixinPlayerListHud(IPlayerListHud):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getHeader(self) -> Text:
		pass

	@overload
	def jsmacros_getFooter(self) -> Text:
		pass

	pass


