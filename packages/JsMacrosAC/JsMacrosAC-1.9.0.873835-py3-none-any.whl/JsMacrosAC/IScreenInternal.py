from typing import overload
from typing import TypeVar

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class IScreenInternal:

	@overload
	def jsmacros_render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def jsmacros_mouseClicked(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_mouseReleased(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> None:
		pass

	@overload
	def jsmacros_mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> None:
		pass

	@overload
	def jsmacros_keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> None:
		pass

	@overload
	def jsmacros_charTyped(self, chr: str, modifiers: int) -> None:
		pass

	pass


