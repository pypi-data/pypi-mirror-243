from typing import overload
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .ScriptTrigger import ScriptTrigger
from .MacroScreen import MacroScreen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

java_io_File = TypeVar("java_io_File")
File = java_io_File

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class MacroContainer(MultiElementContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, macro: ScriptTrigger, parent: MacroScreen) -> None:
		pass

	@overload
	def getRawMacro(self) -> ScriptTrigger:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setEventType(self, type: str) -> None:
		pass

	@overload
	def setFile(self, f: File) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def onKey(self, translationKey: str) -> bool:
		pass

	@overload
	def buildKeyName(self, translationKeys: str) -> Text:
		pass

	@overload
	def setKey(self, translationKeys: str) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


