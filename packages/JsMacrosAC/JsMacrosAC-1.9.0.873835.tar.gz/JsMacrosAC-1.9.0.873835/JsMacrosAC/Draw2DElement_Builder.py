from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D
from .Draw2D import Draw2D


class Draw2DElement_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, parent: IDraw2D, draw2D: Draw2D) -> None:
		pass

	@overload
	def x(self, x: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the draw2D. 
		"""
		pass

	@overload
	def y(self, y: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			y: the y position of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the draw2D. 
		"""
		pass

	@overload
	def pos(self, x: int, y: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the draw2D 
			y: the y position of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def width(self, width: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the draw2D. 
		"""
		pass

	@overload
	def height(self, height: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			height: the height of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the draw2D. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the draw2D 
			height: the height of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def scale(self, scale: float) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			scale: the scale of the draw2D 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of the draw2D. 
		"""
		pass

	@overload
	def rotation(self, rotation: float) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the draw2D in degrees 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the draw2D in degrees. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether this draw2D should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this draw2D should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def zIndex(self, zIndex: int) -> "Draw2DElement_Builder":
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the draw2D. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the draw2D. 
		"""
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
	def moveTo(self, x: int, y: int) -> "Draw2DElement_Builder":
		pass

	pass


