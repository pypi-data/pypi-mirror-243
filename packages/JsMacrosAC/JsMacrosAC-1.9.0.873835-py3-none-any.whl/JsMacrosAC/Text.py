from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .IDraw2D import IDraw2D
from .TextHelper import TextHelper

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class Text(RenderElement, Alignable):
	"""
	Since: 1.0.5 
	"""
	parent: IDraw2D
	text: Text
	scale: float
	rotation: float
	rotateCenter: bool
	x: int
	y: int
	color: int
	width: int
	shadow: bool
	zIndex: int

	@overload
	def __init__(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def __init__(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def setX(self, x: int) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			x: the new x position for this text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of this element. 
		"""
		pass

	@overload
	def setY(self, y: int) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			y: the new y position for this text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of this element. 
		"""
		pass

	@overload
	def setPos(self, x: int, y: int) -> "Text":
		"""
		Since: 1.0.5 

		Args:
			x: 
			y: 
		"""
		pass

	@overload
	def setText(self, text: str) -> "Text":
		"""
		Since: 1.0.5 

		Args:
			text: 
		"""
		pass

	@overload
	def setText(self, text: TextHelper) -> "Text":
		"""
		Since: 1.2.7 

		Args:
			text: 
		"""
		pass

	@overload
	def getText(self) -> TextHelper:
		"""
		Since: 1.2.7 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this text. 
		"""
		pass

	@overload
	def setShadow(self, shadow: bool) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			shadow: whether the text should be rendered with a shadow 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hasShadow(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this text element is rendered with a shadow, 'false' otherwise. 
		"""
		pass

	@overload
	def setScale(self, scale: float) -> "Text":
		"""
		Since: 1.0.5 

		Args:
			scale: 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of this text. 
		"""
		pass

	@overload
	def setRotation(self, rotation: float) -> "Text":
		"""
		Since: 1.0.5 

		Args:
			rotation: 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation of this text. 
		"""
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether this text should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this text should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def setColor(self, color: int) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			color: the new color for this text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of this text. 
		"""
		pass

	@overload
	def setZIndex(self, zIndex: int) -> "Text":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the new z-index for this text element 

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
	def render3D(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def setParent(self, parent: IDraw2D) -> "Text":
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
	def moveTo(self, x: int, y: int) -> "Text":
		pass

	pass


