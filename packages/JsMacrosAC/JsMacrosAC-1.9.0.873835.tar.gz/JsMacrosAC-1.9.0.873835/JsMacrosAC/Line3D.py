from typing import overload
from typing import TypeVar
from .RenderElement3D import RenderElement3D
from .Vec3D import Vec3D

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class Line3D(RenderElement3D):
	"""
	"""
	pos: Vec3D
	color: int
	cull: bool

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, cull: bool) -> None:
		pass

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, cull: bool) -> None:
		pass

	@overload
	def setPos(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
		"""
		Since: 1.0.6 

		Args:
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def setColor(self, color: int) -> None:
		"""
		Since: 1.0.6 

		Args:
			color: 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> None:
		"""
		Since: 1.1.8 

		Args:
			color: 
			alpha: 
		"""
		pass

	@overload
	def setAlpha(self, alpha: int) -> None:
		"""
		Since: 1.1.8 

		Args:
			alpha: 
		"""
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareToSame(self, o: "Line3D") -> int:
		pass

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	pass


