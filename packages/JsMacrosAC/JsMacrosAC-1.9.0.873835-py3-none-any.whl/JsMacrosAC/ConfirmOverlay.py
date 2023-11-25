from typing import overload
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent

java_util_function_Consumer_xyz_wagyourtail_wagyourgui_overlays_ConfirmOverlay_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_wagyourgui_overlays_ConfirmOverlay_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_wagyourgui_overlays_ConfirmOverlay_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class ConfirmOverlay(OverlayContainer):
	hcenter: bool

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, message: Text, parent: IOverlayParent, accept: Consumer) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, hcenter: bool, textRenderer: TextRenderer, message: Text, parent: IOverlayParent, accept: Consumer) -> None:
		pass

	@overload
	def setMessage(self, message: Text) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


