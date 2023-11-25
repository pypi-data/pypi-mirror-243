from typing import overload
from typing import TypeVar

net_minecraft_text_ClickEvent_Action = TypeVar("net_minecraft_text_ClickEvent_Action")
ClickEvent_Action = net_minecraft_text_ClickEvent_Action


class MixinStyleSerializer:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def redirectClickGetAction(self, action: ClickEvent_Action) -> str:
		pass

	pass


