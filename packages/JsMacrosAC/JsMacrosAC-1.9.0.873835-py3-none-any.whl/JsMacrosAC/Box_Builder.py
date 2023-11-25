from typing import overload
from .Draw3D import Draw3D
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .Box import Box


class Box_Builder:
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, parent: Draw3D) -> None:
		pass

	@overload
	def pos1(self, pos1: Pos3D) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos1(self, pos1: BlockPosHelper) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos1(self, x1: float, y1: float, z1: float) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			z1: the z coordinate of the first position of the box 
			y1: the y coordinate of the first position of the box 
			x1: the x coordinate of the first position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPos1(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the first position of the box. 
		"""
		pass

	@overload
	def pos2(self, pos2: Pos3D) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos2: the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos2(self, pos2: BlockPosHelper) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos2: the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos2(self, x2: float, y2: float, z2: float) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			z2: the z coordinate of the second position of the box 
			y2: the y coordinate of the second position of the box 
			x2: the x coordinate of the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPos2(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the second position of the box. 
		"""
		pass

	@overload
	def pos(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			z1: the z coordinate of the first position of the box 
			y1: the y coordinate of the first position of the box 
			z2: the z coordinate of the second position of the box 
			x1: the x coordinate of the first position of the box 
			y2: the y coordinate of the second position of the box 
			x2: the x coordinate of the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, pos1: BlockPosHelper, pos2: BlockPosHelper) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the box 
			pos2: the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, pos1: Pos3D, pos2: Pos3D) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position of the box 
			pos2: the second position of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def forBlock(self, x: int, y: int, z: int) -> "Box_Builder":
		"""Highlights the given block position.\n
		Since: 1.8.4 

		Args:
			x: the x coordinate of the block 
			y: the y coordinate of the block 
			z: the z coordinate of the block 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def forBlock(self, pos: BlockPosHelper) -> "Box_Builder":
		"""Highlights the given block position.\n
		Since: 1.8.4 

		Args:
			pos: the block position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int, alpha: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the fill color of the box 
			alpha: the alpha value for the box's fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			r: the red component of the fill color 
			b: the blue component of the fill color 
			g: the green component of the fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int, a: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			a: the alpha component of the fill color 
			r: the red component of the fill color 
			b: the blue component of the fill color 
			g: the green component of the fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of the box. 
		"""
		pass

	@overload
	def alpha(self, alpha: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			alpha: the alpha value for the box's color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of the box's color. 
		"""
		pass

	@overload
	def fillColor(self, fillColor: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			fillColor: the fill color of the box 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillColor(self, fillColor: int, alpha: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			fillColor: the fill color of the box 
			alpha: the alpha value for the box's fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillColor(self, r: int, g: int, b: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			r: the red component of the fill color 
			b: the blue component of the fill color 
			g: the green component of the fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillColor(self, r: int, g: int, b: int, a: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			a: the alpha component of the fill color 
			r: the red component of the fill color 
			b: the blue component of the fill color 
			g: the green component of the fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getFillColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the fill color of the box. 
		"""
		pass

	@overload
	def fillAlpha(self, fillAlpha: int) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			fillAlpha: the alpha value for the box's fill color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getFillAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of the box's fill color. 
		"""
		pass

	@overload
	def fill(self, fill: bool) -> "Box_Builder":
		"""
		Since: 1.8.4 

		Args:
			fill: 'true' if the box should be filled, 'false' otherwise 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isFilled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the box should be filled, 'false' otherwise. 
		"""
		pass

	@overload
	def cull(self, cull: bool) -> "Box_Builder":
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
	def buildAndAdd(self) -> Box:
		"""Creates the box for the given values and adds it to the draw3D.\n
		Since: 1.8.4 

		Returns:
			the build box. 
		"""
		pass

	@overload
	def build(self) -> Box:
		"""Builds the box from the given values.

		Returns:
			the build box. 
		"""
		pass

	pass


