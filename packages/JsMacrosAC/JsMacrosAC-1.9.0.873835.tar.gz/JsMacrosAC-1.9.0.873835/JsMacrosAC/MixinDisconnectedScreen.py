from typing import overload
from typing import TypeVar

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class MixinDisconnectedScreen:

	@overload
	def getReason(self) -> Text:
		pass

	pass


