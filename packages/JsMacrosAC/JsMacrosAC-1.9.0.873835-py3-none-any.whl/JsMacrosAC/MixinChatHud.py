from typing import overload
from typing import List
from typing import TypeVar
from .IChatHud import IChatHud

net_minecraft_client_gui_hud_ChatHudLine = TypeVar("net_minecraft_client_gui_hud_ChatHudLine")
ChatHudLine = net_minecraft_client_gui_hud_ChatHudLine

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

java_util_function_Predicate_net_minecraft_client_gui_hud_ChatHudLine_ = TypeVar("java_util_function_Predicate_net_minecraft_client_gui_hud_ChatHudLine_")
Predicate = java_util_function_Predicate_net_minecraft_client_gui_hud_ChatHudLine_


class MixinChatHud(IChatHud):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_addMessageBypass(self, message: Text) -> None:
		pass

	@overload
	def jsmacros_getMessages(self) -> List[ChatHudLine]:
		pass

	@overload
	def jsmacros_removeMessageById(self, messageId: int) -> None:
		pass

	@overload
	def jsmacros_addMessageAtIndexBypass(self, message: Text, index: int, time: int) -> None:
		pass

	@overload
	def overrideMessagePos(self, pos: int) -> int:
		pass

	@overload
	def jsmacros_removeMessage(self, index: int) -> None:
		pass

	@overload
	def jsmacros_removeMessageByText(self, text: Text) -> None:
		pass

	@overload
	def jsmacros_removeMessagePredicate(self, textfilter: Predicate) -> None:
		pass

	pass


