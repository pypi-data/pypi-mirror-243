from typing import overload
from typing import TypeVar
from .RenderElement3D import RenderElement3D
from .Pos2D import Pos2D
from .Pos3D import Pos3D

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class TraceLine(RenderElement3D):
	"""
	Since: 1.9.0 
	"""
	screenPos: Pos2D
	pos: Pos3D
	color: int

	@overload
	def __init__(self, x: float, y: float, z: float, color: int) -> None:
		pass

	@overload
	def __init__(self, x: float, y: float, z: float, color: int, alpha: int) -> None:
		pass

	@overload
	def __init__(self, pos: Pos3D, color: int) -> None:
		pass

	@overload
	def __init__(self, pos: Pos3D, color: int, alpha: int) -> None:
		pass

	@overload
	def setPos(self, x: float, y: float, z: float) -> "TraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setPos(self, pos: Pos3D) -> "TraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setColor(self, color: int) -> "TraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> "TraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setAlpha(self, alpha: int) -> "TraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareToSame(self, other: "TraceLine") -> int:
		pass

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	pass


