from typing import overload
from typing import List
from typing import TypeVar
from .BaseScreen import BaseScreen
from .Core import Core
from .ModLoader import ModLoader

net_minecraft_client_option_KeyBinding = TypeVar("net_minecraft_client_option_KeyBinding")
KeyBinding = net_minecraft_client_option_KeyBinding

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_MinecraftClient = TypeVar("net_minecraft_client_MinecraftClient")
MinecraftClient = net_minecraft_client_MinecraftClient

net_minecraft_client_util_InputUtil_Key = TypeVar("net_minecraft_client_util_InputUtil_Key")
InputUtil_Key = net_minecraft_client_util_InputUtil_Key

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

org_slf4j_Logger = TypeVar("org_slf4j_Logger")
Logger = org_slf4j_Logger


class JsMacros:
	MOD_ID: str
	LOGGER: Logger
	keyBinding: KeyBinding
	prevScreen: BaseScreen
	core: Core

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onInitialize(self) -> None:
		pass

	@overload
	def onInitializeClient(self) -> None:
		pass

	@overload
	def getKeyText(self, translationKey: str) -> Text:
		pass

	@overload
	def getScreenName(self, s: Screen) -> str:
		pass

	@overload
	def getLocalizedName(self, keyCode: InputUtil_Key) -> str:
		pass

	@overload
	def getMinecraft(self) -> MinecraftClient:
		pass

	@overload
	def range(self, end: int) -> List[int]:
		pass

	@overload
	def range(self, start: int, end: int) -> List[int]:
		pass

	@overload
	def range(self, start: int, end: int, iter: int) -> List[int]:
		pass

	@overload
	def getModLoader(self) -> ModLoader:
		pass

	pass


