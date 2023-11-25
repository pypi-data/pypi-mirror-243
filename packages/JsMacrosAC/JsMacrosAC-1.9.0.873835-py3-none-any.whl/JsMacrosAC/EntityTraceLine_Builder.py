from typing import overload
from .Pos2D import Pos2D
from .Draw3D import Draw3D
from .EntityHelper import EntityHelper
from .EntityTraceLine import EntityTraceLine


class EntityTraceLine_Builder:
	screenPos: Pos2D

	@overload
	def __init__(self, parent: Draw3D) -> None:
		pass

	@overload
	def entity(self, entity: EntityHelper) -> "EntityTraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			entity: the target entity 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getEntity(self) -> EntityHelper:
		"""
		Since: 1.9.0 

		Returns:
			the target entity 
		"""
		pass

	@overload
	def yOffset(self, yOffset: float) -> "EntityTraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			yOffset: the offset of y-axis 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getYOffset(self) -> float:
		"""
		Since: 1.9.0 

		Returns:
			the offset of y-axis 
		"""
		pass

	@overload
	def color(self, color: int) -> "EntityTraceLine_Builder":
		"""
		Since: 1.9.0 

		Args:
			color: the color of the line 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def color(self, color: int, alpha: int) -> "EntityTraceLine_Builder":
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
	def color(self, r: int, g: int, b: int) -> "EntityTraceLine_Builder":
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
	def color(self, r: int, g: int, b: int, a: int) -> "EntityTraceLine_Builder":
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
	def alpha(self, alpha: int) -> "EntityTraceLine_Builder":
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
	def buildAndAdd(self, entity: EntityHelper) -> EntityTraceLine:
		"""Creates the trace line for the given values and adds it to the draw3D\n
		Since: 1.9.0 

		Args:
			entity: the target entity 

		Returns:
			the build line 
		"""
		pass

	@overload
	def buildAndAdd(self) -> EntityTraceLine:
		"""Creates the trace line for the given values and adds it to the draw3D\n
		Since: 1.9.0 

		Returns:
			the build line 
		"""
		pass

	@overload
	def build(self, entity: EntityHelper) -> EntityTraceLine:
		"""Builds the line from the given values\n
		Since: 1.9.0 

		Args:
			entity: the target entity 

		Returns:
			the build line 
		"""
		pass

	@overload
	def build(self) -> EntityTraceLine:
		"""Builds the line from the given values\n
		Since: 1.9.0 

		Returns:
			the build line 
		"""
		pass

	pass


