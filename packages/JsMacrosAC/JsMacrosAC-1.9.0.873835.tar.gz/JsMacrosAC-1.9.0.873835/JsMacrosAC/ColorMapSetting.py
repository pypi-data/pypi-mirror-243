from typing import overload
from typing import List
from typing import TypeVar
from .AbstractMapSettingContainer import AbstractMapSettingContainer
from .SettingsOverlay import SettingsOverlay

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ColorMapSetting(AbstractMapSettingContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addField(self, key: str, value: List[float]) -> None:
		pass

	pass


