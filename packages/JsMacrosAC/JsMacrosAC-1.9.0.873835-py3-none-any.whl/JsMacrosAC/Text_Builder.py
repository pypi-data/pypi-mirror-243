from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D
from .TextHelper import TextHelper
from .TextBuilder import TextBuilder
from .Text import Text


class Text_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, draw2D: IDraw2D) -> None:
		pass

	@overload
	def text(self, text: TextHelper) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			text: the content of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def text(self, text: TextBuilder) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			text: the content of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def text(self, text: str) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			text: the content of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getText(self) -> TextHelper:
		"""
		Since: 1.8.4 

		Returns:
			the content of the text element. 
		"""
		pass

	@overload
	def x(self, x: int) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the text element. 
		"""
		pass

	@overload
	def y(self, y: int) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			y: the y position of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the text element. 
		"""
		pass

	@overload
	def pos(self, x: int, y: int) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the text element 
			y: the y position of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the string. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the string. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Text_Builder":
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
	def color(self, r: int, g: int, b: int, a: int) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			a: the alpha component of the color 
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
			the color of the text element. 
		"""
		pass

	@overload
	def scale(self, scale: float) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			scale: the scale of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of the text element. 
		"""
		pass

	@overload
	def rotation(self, rotation: float) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the text element in degrees 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the text element in degrees. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Text_Builder":
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
	def shadow(self, shadow: bool) -> "Text_Builder":
		"""
		Since: 1.8.4 

		Args:
			shadow: whether the text should have a shadow or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def hasShadow(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the text element has a shadow, 'false' otherwise. 
		"""
		pass

	@overload
	def zIndex(self, zIndex: int) -> "Text_Builder":
		"""

		Args:
			zIndex: the z-index of the text element 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the text element. 
		"""
		pass

	@overload
	def createElement(self) -> Text:
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
	def moveTo(self, x: int, y: int) -> "Text_Builder":
		pass

	pass


