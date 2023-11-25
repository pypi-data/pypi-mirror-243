from typing import overload
from typing import List
from typing import TypeVar
from .AbstractMapSettingContainer import AbstractMapSettingContainer
from .SettingsOverlay import SettingsOverlay
from .ScriptTrigger import ScriptTrigger

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ProfileSetting(AbstractMapSettingContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addField(self, key: str, value: List[ScriptTrigger]) -> None:
		pass

	@overload
	def removeField(self, key: str) -> None:
		pass

	@overload
	def changeKey(self, key: str, newKey: str) -> None:
		pass

	pass


