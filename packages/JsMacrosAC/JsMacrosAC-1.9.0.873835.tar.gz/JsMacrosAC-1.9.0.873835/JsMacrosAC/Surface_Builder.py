from typing import overload
from .Draw3D import Draw3D
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .EntityHelper import EntityHelper
from .Surface import Surface


class Surface_Builder:
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, parent: Draw3D) -> None:
		pass

	@overload
	def pos(self, pos: Pos3D) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos: the position of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, pos: BlockPosHelper) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos: the position of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, x: float, y: float, z: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the surface 
			y: the y position of the surface 
			z: the z position of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPos(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the position of the surface. 
		"""
		pass

	@overload
	def bindToEntity(self, boundEntity: EntityHelper) -> "Surface_Builder":
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
	def boundOffset(self, entityOffset: Pos3D) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			entityOffset: the offset from the entity's position to render the surface at 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def boundOffset(self, x: float, y: float, z: float) -> "Surface_Builder":
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
	def xRotation(self, xRot: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			xRot: the x rotation of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getXRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the x rotation of the surface. 
		"""
		pass

	@overload
	def yRotation(self, yRot: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			yRot: the y rotation of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getYRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the y rotation of the surface. 
		"""
		pass

	@overload
	def zRotation(self, zRot: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			zRot: the z rotation of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the z rotation of the surface. 
		"""
		pass

	@overload
	def rotation(self, xRot: float, yRot: float, zRot: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			zRot: the z rotation of the surface 
			yRot: the y rotation of the surface 
			xRot: the x rotation of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether to rotate around the center of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this surface should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def rotateToPlayer(self, rotateToPlayer: bool) -> "Surface_Builder":
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
	def width(self, width: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the width of the surface. 
		"""
		pass

	@overload
	def height(self, height: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			height: the height of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the height of the surface. 
		"""
		pass

	@overload
	def size(self, width: float, height: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the surface 
			height: the height of the surface 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def minSubdivisions(self, minSubdivisions: int) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			minSubdivisions: the minimum number of subdivisions 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMinSubdivisions(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the minimum number of subdivisions. 
		"""
		pass

	@overload
	def renderBack(self, renderBack: bool) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			renderBack: whether the back of the surface should be rendered or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def shouldRenderBack(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the back of the surface should be rendered, 'false' otherwise. 
		"""
		pass

	@overload
	def cull(self, cull: bool) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			cull: whether to enable culling or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isCulled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if culling is enabled for this box, 'false' otherwise. 
		"""
		pass

	@overload
	def zIndex(self, zIndexScale: float) -> "Surface_Builder":
		"""
		Since: 1.8.4 

		Args:
			zIndexScale: the scale of the z-index 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndexScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of the z-index. 
		"""
		pass

	@overload
	def buildAndAdd(self) -> Surface:
		"""Creates the surface for the given values and adds it to the draw3D.\n
		Since: 1.8.4 

		Returns:
			the build surface. 
		"""
		pass

	@overload
	def build(self) -> Surface:
		"""Builds the surface from the given values.

		Returns:
			the build surface. 
		"""
		pass

	pass


