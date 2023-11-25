from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D
from .Rect import Rect


class Rect_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, draw2D: IDraw2D) -> None:
		pass

	@overload
	def x1(self, x1: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			x1: the first x position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first x position of the rectangle. 
		"""
		pass

	@overload
	def y1(self, y1: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first y position of the rectangle. 
		"""
		pass

	@overload
	def pos1(self, x1: int, y1: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of the rectangle 
			x1: the first x position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def x2(self, x2: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			x2: the second x position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the second x position of the rectangle. 
		"""
		pass

	@overload
	def y2(self, y2: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			y2: the second y position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the second y position of the rectangle. 
		"""
		pass

	@overload
	def pos2(self, x2: int, y2: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			y2: the second y position of the rectangle 
			x2: the second x position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, x1: int, y1: int, x2: int, y2: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of the rectangle 
			x1: the first x position of the rectangle 
			y2: the second y position of the rectangle 
			x2: the second x position of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def width(self, width: int) -> "Rect_Builder":
		"""The width will just set the x2 position to 'x1 + width' .\n
		Since: 1.8.4 

		Args:
			width: the width of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the rectangle. 
		"""
		pass

	@overload
	def height(self, height: int) -> "Rect_Builder":
		"""The width will just set the y2 position to 'y1 + height' .\n
		Since: 1.8.4 

		Args:
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the rectangle. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the rectangle 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Rect_Builder":
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
	def color(self, r: int, g: int, b: int, a: int) -> "Rect_Builder":
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
	def color(self, color: int, alpha: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the rectangle 
			alpha: the alpha value of the color 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of the rectangle. 
		"""
		pass

	@overload
	def alpha(self, alpha: int) -> "Rect_Builder":
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
	def rotation(self, rotation: float) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the rectangle in degrees 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the rectangle in degrees. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether this rectangle should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this rectangle should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def zIndex(self, zIndex: int) -> "Rect_Builder":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the rectangle. 
		"""
		pass

	@overload
	def createElement(self) -> Rect:
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

	@overload
	def moveTo(self, x: int, y: int) -> "Rect_Builder":
		pass

	pass


