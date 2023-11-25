from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .IDraw2D import IDraw2D

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Line(RenderElement, Alignable):
	"""
	Since: 1.8.4 
	"""
	parent: IDraw2D
	x1: int
	y1: int
	x2: int
	y2: int
	color: int
	rotation: float
	rotateCenter: bool
	width: float
	zIndex: int

	@overload
	def __init__(self, x1: int, y1: int, x2: int, y2: int, color: int, rotation: float, width: float, zIndex: int) -> None:
		pass

	@overload
	def setX1(self, x1: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			x1: the x position of the start of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the start of the line. 
		"""
		pass

	@overload
	def setY1(self, y1: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the start of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY1(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the start of the line. 
		"""
		pass

	@overload
	def setPos1(self, x1: int, y1: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the start of the line 
			x1: the x position of the start of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setX2(self, x2: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			x2: the x position of the end of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the end of the line. 
		"""
		pass

	@overload
	def setY2(self, y2: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			y2: the y position of the end of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY2(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the end of the line. 
		"""
		pass

	@overload
	def setPos2(self, x2: int, y2: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			y2: the y position of the end of the line 
			x2: the x position of the end of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPos(self, x1: int, y1: int, x2: int, y2: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the start of the line 
			x1: the x position of the start of the line 
			y2: the y position of the end of the line 
			x2: the x position of the end of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setColor(self, color: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line 
			alpha: the alpha of the line 

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
	def setAlpha(self, alpha: int) -> "Line":
		"""
		Since: 1.8.4 

		Args:
			alpha: the alpha value of the line's color 

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
	def setRotation(self, rotation: float) -> "Line":
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
	def setRotateCenter(self, rotateCenter: bool) -> "Line":
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
	def setWidth(self, width: float) -> "Line":
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
	def setZIndex(self, zIndex: int) -> "Line":
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
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def setParent(self, parent: IDraw2D) -> "Line":
		pass

	@overload
	def moveTo(self, x: int, y: int) -> "Line":
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


