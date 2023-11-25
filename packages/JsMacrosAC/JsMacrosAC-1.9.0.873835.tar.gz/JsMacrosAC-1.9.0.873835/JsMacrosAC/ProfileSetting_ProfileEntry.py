from typing import overload
from typing import List
from typing import TypeVar
from .AbstractMapSettingContainer_MapSettingEntry import AbstractMapSettingContainer_MapSettingEntry
from .ProfileSetting import ProfileSetting
from .ScriptTrigger import ScriptTrigger

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ProfileSetting_ProfileEntry(AbstractMapSettingContainer_MapSettingEntry):

	@overload
	def __init__(self, x: int, y: int, width: int, textRenderer: TextRenderer, parent: ProfileSetting, key: str, value: List[ScriptTrigger]) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	pass


