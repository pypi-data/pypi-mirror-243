from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .AbstractSettingContainer import AbstractSettingContainer
from .SettingsOverlay_SettingField import SettingsOverlay_SettingField
from .SettingsOverlay import SettingsOverlay

T = TypeVar("T")
U = TypeVar("U")
net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_OrderedText = TypeVar("net_minecraft_text_OrderedText")
OrderedText = net_minecraft_text_OrderedText

java_util_function_Supplier_T_ = TypeVar("java_util_function_Supplier_T_")
Supplier = java_util_function_Supplier_T_

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class AbstractMapSettingContainer(Generic[T, U], AbstractSettingContainer):
	setting: SettingsOverlay_SettingField
	settingName: OrderedText
	map: Mapping[str, U]
	topScroll: int
	totalHeight: int
	defaultValue: Supplier

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def onScrollbar(self, pages: float) -> None:
		pass

	@overload
	def newField(self, key: str) -> None:
		pass

	@overload
	def addField(self, key: str, value: T) -> None:
		pass

	@overload
	def removeField(self, key: str) -> None:
		pass

	@overload
	def changeValue(self, key: str, newValue: T) -> None:
		pass

	@overload
	def changeKey(self, key: str, newKey: str) -> None:
		pass

	@overload
	def addSetting(self, setting: SettingsOverlay_SettingField) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


