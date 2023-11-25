from typing import overload
from .Draw3D import Draw3D
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .Line3D import Line3D


class Line3D_Builder:
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, parent: Draw3D) -> None:
		pass

	@overload
	def pos1(self, pos1: Pos3D) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos1(self, pos1: BlockPosHelper) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos1(self, x1: float, y1: float, z1: float) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			z1: the z coordinate of the first position of the line 
			y1: the y coordinate of the first position of the line 
			x1: the x coordinate of the first position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPos1(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the first position of the line. 
		"""
		pass

	@overload
	def pos2(self, pos2: Pos3D) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos2: the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos2(self, pos2: BlockPosHelper) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos2: the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos2(self, x2: int, y2: int, z2: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			z2: the z coordinate of the second position of the line 
			y2: the y coordinate of the second position of the line 
			x2: the x coordinate of the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPos2(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the second position of the line. 
		"""
		pass

	@overload
	def pos(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			z1: the z coordinate of the first position of the line 
			y1: the y coordinate of the first position of the line 
			z2: the z coordinate of the second position of the line 
			x1: the x coordinate of the first position of the line 
			y2: the x coordinate of the second position of the line 
			x2: the x coordinate of the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, pos1: BlockPosHelper, pos2: BlockPosHelper) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the line 
			pos2: the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, pos1: Pos3D, pos2: Pos3D) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the line 
			pos2: the second position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int, alpha: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 
			alpha: the alpha value of the line's color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			r: the red component of the color 
			b: the blue component of the color 
			g: the green component of the color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int, a: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			a: the alpha value of the color 
			r: the red component of the color 
			b: the blue component of the color 
			g: the green component of the color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of the line. 
		"""
		pass

	@overload
	def alpha(self, alpha: int) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			alpha: the alpha value for the line's color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of the line's color. 
		"""
		pass

	@overload
	def cull(self, cull: bool) -> "Line3D_Builder":
		"""
		Since: 1.8.4 

		Args:
			cull: whether to cull the line or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isCulled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the line should be culled, 'false' otherwise. 
		"""
		pass

	@overload
	def buildAndAdd(self) -> Line3D:
		"""Creates the line for the given values and adds it to the draw3D.\n
		Since: 1.8.4 

		Returns:
			the build line. 
		"""
		pass

	@overload
	def build(self) -> Line3D:
		"""Builds the line from the given values.

		Returns:
			the build line. 
		"""
		pass

	pass


