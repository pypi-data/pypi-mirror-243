from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .IDraw2D import IDraw2D

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Image(RenderElement, Alignable):
	"""
	Since: 1.2.3 
	"""
	parent: IDraw2D
	rotation: float
	rotateCenter: bool
	x: int
	y: int
	width: int
	height: int
	imageX: int
	imageY: int
	regionWidth: int
	regionHeight: int
	textureWidth: int
	textureHeight: int
	color: int
	zIndex: int

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, zIndex: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, zIndex: int, alpha: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> None:
		pass

	@overload
	def setImage(self, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> "Image":
		"""
		Since: 1.2.3 

		Args:
			imageY: 
			textureWidth: 
			imageX: 
			regionHeight: 
			id: 
			regionWidth: 
			textureHeight: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getImage(self) -> str:
		"""
		Since: 1.2.3 
		"""
		pass

	@overload
	def setX(self, x: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			x: the new x position of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of this image. 
		"""
		pass

	@overload
	def setY(self, y: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			y: the new y position of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of this image. 
		"""
		pass

	@overload
	def setPos(self, x: int, y: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			x: the new x position of this image 
			y: the new y position of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> "Image":
		"""
		Since: 1.2.3 

		Args:
			x: 
			width: 
			y: 
			height: 
		"""
		pass

	@overload
	def setWidth(self, width: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			width: the new width of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of this image. 
		"""
		pass

	@overload
	def setHeight(self, height: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			height: the new height of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this image. 
		"""
		pass

	@overload
	def setSize(self, width: int, height: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			width: the new width of this image 
			height: the new height of this image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setColor(self, color: int) -> "Image":
		"""
		Since: 1.6.5 

		Args:
			color: 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> "Image":
		"""
		Since: 1.6.5 

		Args:
			color: 
			alpha: 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of this image. 
		"""
		pass

	@overload
	def getAlpha(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of this image. 
		"""
		pass

	@overload
	def setRotation(self, rotation: float) -> "Image":
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
			the rotation of this image. 
		"""
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether the image should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this image should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def setZIndex(self, zIndex: int) -> "Image":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the new z-index of this image 

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
	def setParent(self, parent: IDraw2D) -> "Image":
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
	def moveTo(self, x: int, y: int) -> "Image":
		pass

	pass


