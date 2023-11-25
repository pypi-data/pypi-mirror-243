from typing import overload
from typing import TypeVar
from .IOverlayParent import IOverlayParent
from .OverlayContainer import OverlayContainer

T = TypeVar("T")
net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_gui_Element = TypeVar("net_minecraft_client_gui_Element")
Element = net_minecraft_client_gui_Element

net_minecraft_text_StringVisitable = TypeVar("net_minecraft_text_StringVisitable")
StringVisitable = net_minecraft_text_StringVisitable

net_minecraft_text_OrderedText = TypeVar("net_minecraft_text_OrderedText")
OrderedText = net_minecraft_text_OrderedText

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class BaseScreen(IOverlayParent, Screen):

	@overload
	def trimmed(self, textRenderer: TextRenderer, str: StringVisitable, width: int) -> OrderedText:
		pass

	@overload
	def setParent(self, parent: Screen) -> None:
		pass

	@overload
	def reload(self) -> None:
		pass

	@overload
	def removed(self) -> None:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def getFirstOverlayParent(self) -> IOverlayParent:
		pass

	@overload
	def getChildOverlay(self) -> OverlayContainer:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer, disableButtons: bool) -> None:
		pass

	@overload
	def closeOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def remove(self, btn: Element) -> None:
		pass

	@overload
	def addDrawableChild(self, drawableElement: T) -> T:
		pass

	@overload
	def setFocused(self, focused: Element) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> bool:
		pass

	@overload
	def mouseClicked(self, mouseX: float, mouseY: float, button: int) -> bool:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def shouldCloseOnEsc(self) -> bool:
		pass

	@overload
	def updateSettings(self) -> None:
		pass

	@overload
	def close(self) -> None:
		pass

	@overload
	def openParent(self) -> None:
		pass

	pass


