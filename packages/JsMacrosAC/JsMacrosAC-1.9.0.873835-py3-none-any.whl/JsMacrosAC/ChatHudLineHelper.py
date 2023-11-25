from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

net_minecraft_client_gui_hud_ChatHudLine = TypeVar("net_minecraft_client_gui_hud_ChatHudLine")
ChatHudLine = net_minecraft_client_gui_hud_ChatHudLine

net_minecraft_client_gui_hud_ChatHud = TypeVar("net_minecraft_client_gui_hud_ChatHud")
ChatHud = net_minecraft_client_gui_hud_ChatHud


class ChatHudLineHelper(BaseHelper):

	@overload
	def __init__(self, base: ChatHudLine, hud: ChatHud) -> None:
		pass

	@overload
	def getText(self) -> TextHelper:
		pass

	@overload
	def getCreationTick(self) -> int:
		pass

	@overload
	def deleteById(self) -> "ChatHudLineHelper":
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


