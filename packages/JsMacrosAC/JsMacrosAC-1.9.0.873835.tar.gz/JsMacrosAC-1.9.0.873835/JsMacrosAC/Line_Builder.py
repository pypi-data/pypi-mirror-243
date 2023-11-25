from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D


class Line_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, draw2D: IDraw2D) -> None:
		pass

	@overload
	def x1(self, x1: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			x1: the x position of the first point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the first point. 
		"""
		pass

	@overload
	def y1(self, y1: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the first point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the first point. 
		"""
		pass

	@overload
	def pos1(self, x1: int, y1: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the first point 
			x1: the x position of the first point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def x2(self, x2: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			x2: the x position of the second point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the second point. 
		"""
		pass

	@overload
	def y2(self, y2: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			y2: the y position of the second point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the second point. 
		"""
		pass

	@overload
	def pos2(self, x2: int, y2: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			y2: the y position of the second point 
			x2: the x position of the second point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, x1: int, y1: int, x2: int, y2: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the first point 
			x1: the x position of the first point 
			y2: the y position of the second point 
			x2: the x position of the second point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def rotation(self, rotation: float) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the line. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether this line should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this line should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def width(self, width: float) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the width of the line. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int, alpha: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 
			alpha: the alpha component of the color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Line_Builder":
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
	def color(self, r: int, g: int, b: int, a: int) -> "Line_Builder":
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
	def alpha(self, alpha: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			alpha: the alpha value of the color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of the color. 
		"""
		pass

	@overload
	def zIndex(self, zIndex: int) -> "Line_Builder":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the line. 
		"""
		pass

	@overload
	def moveTo(self, x: int, y: int) -> "Line_Builder":
		pass

	@overload
	def getScaledWidth(self) -> int:
		pass

	@overload
	def getParentWidth(self) -> int:
		pass

	@overload
	def getScaledHeight(self) -> int:
		pass

	@overload
	def getParentHeight(self) -> int:
		pass

	@overload
	def getScaledLeft(self) -> int:
		pass

	@overload
	def getScaledTop(self) -> int:
		pass

	pass


