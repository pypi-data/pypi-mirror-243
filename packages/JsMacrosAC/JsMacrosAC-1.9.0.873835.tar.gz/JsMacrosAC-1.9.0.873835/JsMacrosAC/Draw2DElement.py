from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .Draw2D import Draw2D
from .IDraw2D import IDraw2D

java_util_function_IntSupplier = TypeVar("java_util_function_IntSupplier")
IntSupplier = java_util_function_IntSupplier

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Draw2DElement(RenderElement, Alignable):
	"""
	Since: 1.8.4 
	"""
	draw2D: Draw2D
	parent: IDraw2D
	x: int
	y: int
	width: IntSupplier
	height: IntSupplier
	scale: float
	rotation: float
	rotateCenter: bool
	zIndex: int

	@overload
	def __init__(self, draw2D: Draw2D, x: int, y: int, width: IntSupplier, height: IntSupplier, zIndex: int, scale: float, rotation: float) -> None:
		pass

	@overload
	def getDraw2D(self) -> Draw2D:
		"""
		Since: 1.8.4 

		Returns:
			the internal draw2D this draw2D element is wrapping. 
		"""
		pass

	@overload
	def setX(self, x: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			x: the x position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of this draw2D. 
		"""
		pass

	@overload
	def setY(self, y: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			y: the y position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of this draw2D. 
		"""
		pass

	@overload
	def setPos(self, x: int, y: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			x: the x position 
			y: the y position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setWidth(self, width: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			width: the width 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of this draw2D. 
		"""
		pass

	@overload
	def setHeight(self, height: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			height: the height 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this draw2D. 
		"""
		pass

	@overload
	def setSize(self, width: int, height: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			width: the width 
			height: the height 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setScale(self, scale: float) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			scale: the scale 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of this draw2D. 
		"""
		pass

	@overload
	def setRotation(self, rotation: float) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation of this draw2D. 
		"""
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Draw2DElement":
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
	def setZIndex(self, zIndex: int) -> "Draw2DElement":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of this draw2D 

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
	def setParent(self, parent: IDraw2D) -> "Draw2DElement":
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
	def moveTo(self, x: int, y: int) -> "Draw2DElement":
		pass

	pass


