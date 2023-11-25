from typing import overload
from typing import TypeVar
from typing import Mapping
from .IOverlayParent import IOverlayParent
from .MultiElementContainer import MultiElementContainer
from .Scrollbar import Scrollbar

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_gui_Element = TypeVar("net_minecraft_client_gui_Element")
Element = net_minecraft_client_gui_Element

net_minecraft_client_gui_widget_ClickableWidget = TypeVar("net_minecraft_client_gui_widget_ClickableWidget")
ClickableWidget = net_minecraft_client_gui_widget_ClickableWidget

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class OverlayContainer(IOverlayParent, MultiElementContainer):
	savedBtnStates: Mapping[ClickableWidget, bool]
	scroll: Scrollbar

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: IOverlayParent) -> None:
		pass

	@overload
	def remove(self, btn: Element) -> None:
		pass

	@overload
	def openOverlay(self, overlay: "OverlayContainer") -> None:
		pass

	@overload
	def getFirstOverlayParent(self) -> IOverlayParent:
		pass

	@overload
	def openOverlay(self, overlay: "OverlayContainer", disableButtons: bool) -> None:
		pass

	@overload
	def getChildOverlay(self) -> "OverlayContainer":
		pass

	@overload
	def closeOverlay(self, overlay: "OverlayContainer") -> None:
		pass

	@overload
	def setFocused(self, focused: Element) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		"""

		Returns:
			true if should be handled by overlay 
		"""
		pass

	@overload
	def close(self) -> None:
		pass

	@overload
	def onClose(self) -> None:
		pass

	@overload
	def renderBackground(self, drawContext: DrawContext) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


