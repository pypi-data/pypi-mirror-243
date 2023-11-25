from typing import overload
from typing import TypeVar
from typing import Generic

T = TypeVar("T")
net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class RenderElement3D(Comparable, Generic[T]):

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	@overload
	def compareTo(self, o: "RenderElement3D") -> int:
		pass

	@overload
	def compareToSame(self, other: T) -> int:
		pass

	pass


