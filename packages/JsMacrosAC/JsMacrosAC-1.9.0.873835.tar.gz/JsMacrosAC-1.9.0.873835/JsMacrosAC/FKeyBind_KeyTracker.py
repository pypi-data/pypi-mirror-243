from typing import overload
from typing import TypeVar
from typing import Set

net_minecraft_client_option_KeyBinding = TypeVar("net_minecraft_client_option_KeyBinding")
KeyBinding = net_minecraft_client_option_KeyBinding

net_minecraft_client_util_InputUtil_Key = TypeVar("net_minecraft_client_util_InputUtil_Key")
InputUtil_Key = net_minecraft_client_util_InputUtil_Key


class FKeyBind_KeyTracker:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def press(self, key: InputUtil_Key) -> None:
		pass

	@overload
	def press(self, bind: KeyBinding) -> None:
		pass

	@overload
	def unpress(self, key: InputUtil_Key) -> None:
		pass

	@overload
	def unpress(self, bind: KeyBinding) -> None:
		pass

	@overload
	def getPressedKeys(self) -> Set[str]:
		pass

	pass


