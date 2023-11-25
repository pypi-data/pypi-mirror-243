from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .IDraw2D import IDraw2D

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Rect(RenderElement, Alignable):
	"""
	Since: 1.0.5 
	"""
	parent: IDraw2D
	rotation: float
	rotateCenter: bool
	x1: int
	y1: int
	x2: int
	y2: int
	color: int
	zIndex: int

	@overload
	def __init__(self, x1: int, y1: int, x2: int, y2: int, color: int, rotation: float, zIndex: int) -> None:
		pass

	@overload
	def __init__(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float, zIndex: int) -> None:
		pass

	@overload
	def setX1(self, x1: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			x1: the first x position of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first x position of this rectangle. 
		"""
		pass

	@overload
	def setY1(self, y1: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the first y position of this rectangle. 
		"""
		pass

	@overload
	def setPos1(self, x1: int, y1: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of this rectangle 
			x1: the first x position of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setX2(self, x2: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			x2: the second x position of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the second x position of this rectangle. 
		"""
		pass

	@overload
	def setY2(self, y2: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			y2: the second y position of this rectangle 

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
	def setPos2(self, x2: int, y2: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			y2: the second y position of this rectangle 
			x2: the second x position of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPos(self, x1: int, y1: int, x2: int, y2: int) -> "Rect":
		"""
		Since: 1.1.8 

		Args:
			y1: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def setWidth(self, width: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			width: the new width of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of this rectangle. 
		"""
		pass

	@overload
	def setHeight(self, height: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			height: the new height of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this rectangle. 
		"""
		pass

	@overload
	def setSize(self, width: int, height: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			width: the new width of this rectangle 
			height: the new height of this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setColor(self, color: int) -> "Rect":
		"""
		Since: 1.0.5 

		Args:
			color: 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> "Rect":
		"""
		Since: 1.1.8 

		Args:
			color: 
			alpha: 
		"""
		pass

	@overload
	def setAlpha(self, alpha: int) -> "Rect":
		"""
		Since: 1.1.8 

		Args:
			alpha: 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color value of this rectangle. 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of this rectangle. 
		"""
		pass

	@overload
	def setRotation(self, rotation: float) -> "Rect":
		"""
		Since: 1.2.6 

		Args:
			rotation: 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation of this rectangle. 
		"""
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Rect":
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
	def setZIndex(self, zIndex: int) -> "Rect":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the new z-index for this rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def setParent(self, parent: IDraw2D) -> "Rect":
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
	def moveTo(self, x: int, y: int) -> "Rect":
		pass

	pass


