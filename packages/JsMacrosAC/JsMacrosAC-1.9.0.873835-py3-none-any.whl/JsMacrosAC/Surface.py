from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .RenderElement3D import RenderElement3D
from .Draw2D import Draw2D
from .EntityHelper import EntityHelper
from .Pos3D import Pos3D
from .Pos2D import Pos2D
from .BlockPosHelper import BlockPosHelper

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class Surface(RenderElement, RenderElement3D, Draw2D):
	"""
	Since: 1.6.5 
	"""
	rotateToPlayer: bool
	rotateCenter: bool
	boundEntity: EntityHelper
	boundOffset: Pos3D
	pos: Pos3D
	rotations: Pos3D
	zIndexScale: float
	renderBack: bool
	cull: bool

	@overload
	def __init__(self, pos: Pos3D, rotations: Pos3D, sizes: Pos2D, minSubdivisions: int, renderBack: bool, cull: bool) -> None:
		pass

	@overload
	def setPos(self, pos: Pos3D) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			pos: the position of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPos(self, pos: BlockPosHelper) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			pos: the position of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPos(self, x: float, y: float, z: float) -> "Surface":
		pass

	@overload
	def bindToEntity(self, boundEntity: EntityHelper) -> "Surface":
		"""The surface will move with the entity at the offset location.\n
		Since: 1.8.4 

		Args:
			boundEntity: the entity to bind the surface to 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getBoundEntity(self) -> EntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the entity the surface is bound to, or 'null' if it is not bound to an
entity. 
		"""
		pass

	@overload
	def setBoundOffset(self, boundOffset: Pos3D) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			boundOffset: the offset from the entity's position to render the surface at 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setBoundOffset(self, x: float, y: float, z: float) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			x: the x offset from the entity's position to render the surface at 
			y: the y offset from the entity's position to render the surface at 
			z: the z offset from the entity's position to render the surface at 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getBoundOffset(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the offset from the entity's position to render the surface at. 
		"""
		pass

	@overload
	def setRotateToPlayer(self, rotateToPlayer: bool) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			rotateToPlayer: whether to rotate the surface to face the player or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def doesRotateToPlayer(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the surface should be rotated to face the player, 'false' otherwise. 
		"""
		pass

	@overload
	def setRotations(self, x: float, y: float, z: float) -> None:
		pass

	@overload
	def setSizes(self, x: float, y: float) -> None:
		pass

	@overload
	def getSizes(self) -> Pos2D:
		pass

	@overload
	def setMinSubdivisions(self, minSubdivisions: int) -> None:
		pass

	@overload
	def getMinSubdivisions(self) -> int:
		pass

	@overload
	def getHeight(self) -> int:
		pass

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Surface":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether to rotate the surface around its center or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this surface is rotated around it's center, 'false' otherwise. 
		"""
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareToSame(self, other: "Surface") -> int:
		pass

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, delta: float) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


