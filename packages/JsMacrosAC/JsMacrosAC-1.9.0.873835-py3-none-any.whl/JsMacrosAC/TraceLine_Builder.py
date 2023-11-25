from typing import overload
from .Pos2D import Pos2D
from .Draw3D import Draw3D
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .TraceLine import TraceLine


class TraceLine_Builder:
	screenPos: Pos2D

	@overload
	def __init__(self, parent: Draw3D) -> None:
		pass

	@overload
	def pos(self, pos: Pos3D) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			pos: the position of the target 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def pos(self, pos: BlockPosHelper) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			pos: the position of the target 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def pos(self, x: int, y: int, z: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			x: the x coordinate of the target 
			y: the y coordinate of the target 
			z: the z coordinate of the target 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getPos(self) -> Pos3D:
		"""
		Since: 1.9.0 

		Returns:
			the position of the target 
		"""
		pass

	@overload
	def color(self, color: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			color: the color of the line 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def color(self, color: int, alpha: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			color: the color of the line 
			alpha: the alpha value of the line's color 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			r: the red component of the color 
			b: the blue component of the color 
			g: the green component of the color 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int, a: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			a: the alpha value of the color 
			r: the red component of the color 
			b: the blue component of the color 
			g: the green component of the color 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.9.0 

		Returns:
			the color of the line 
		"""
		pass

	@overload
	def alpha(self, alpha: int) -> "TraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			alpha: the alpha value for the line's color 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.9.0 

		Returns:
			the alpha value of the line's color 
		"""
		pass

	@overload
	def buildAndAdd(self) -> TraceLine:
		"""Creates the trace line for the given values and adds it to the draw3D\n
		Since: 1.9.0 

		Returns:
			the build line 
		"""
		pass

	@overload
	def build(self) -> TraceLine:
		"""Builds the line from the given values\n
		Since: 1.9.0 

		Returns:
			the build line 
		"""
		pass

	pass


