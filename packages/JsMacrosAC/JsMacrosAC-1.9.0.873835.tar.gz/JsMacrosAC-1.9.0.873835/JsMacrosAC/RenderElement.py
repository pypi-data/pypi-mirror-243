from typing import overload
from typing import TypeVar

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_util_math_MatrixStack = TypeVar("net_minecraft_client_util_math_MatrixStack")
MatrixStack = net_minecraft_client_util_math_MatrixStack

net_minecraft_client_MinecraftClient = TypeVar("net_minecraft_client_MinecraftClient")
MinecraftClient = net_minecraft_client_MinecraftClient

net_minecraft_client_gui_Drawable = TypeVar("net_minecraft_client_gui_Drawable")
Drawable = net_minecraft_client_gui_Drawable


class RenderElement(Drawable):
	"""
	"""
	mc: MinecraftClient

	@overload
	def getZIndex(self) -> int:
		pass

	@overload
	def render3D(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def setupMatrix(self, matrices: MatrixStack, x: float, y: float, scale: float, rotation: float) -> None:
		pass

	@overload
	def setupMatrix(self, matrices: MatrixStack, x: float, y: float, scale: float, rotation: float, width: float, height: float, rotateAroundCenter: bool) -> None:
		pass

	pass


