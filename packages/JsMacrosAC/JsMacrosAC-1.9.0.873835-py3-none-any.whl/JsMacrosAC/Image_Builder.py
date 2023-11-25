from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D
from .CustomImage import CustomImage
from .Image import Image


class Image_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, draw2D: IDraw2D) -> None:
		pass

	@overload
	def fromCustomImage(self, customImage: CustomImage) -> "Image_Builder":
		"""Will automatically set all attributes to the default values of the custom image.
Values set before the call of this method will be overwritten.\n
		Since: 1.8.4 

		Args:
			customImage: the custom image to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def identifier(self, identifier: str) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			identifier: the identifier of the image to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getIdentifier(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of the used image or 'null' if no image is used. 
		"""
		pass

	@overload
	def x(self, x: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the image. 
		"""
		pass

	@overload
	def y(self, y: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			y: the y position of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the image. 
		"""
		pass

	@overload
	def pos(self, x: int, y: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the image 
			y: the y position of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def width(self, width: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the image. 
		"""
		pass

	@overload
	def height(self, height: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			height: the height of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the image. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the image 
			height: the height of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def imageX(self, imageX: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			imageX: the x position in the image texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getImageX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position in the image texture to start drawing from. 
		"""
		pass

	@overload
	def imageY(self, imageY: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			imageY: the y position in the image texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getImageY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position in the image texture to start drawing from. 
		"""
		pass

	@overload
	def imagePos(self, imageX: int, imageY: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			imageY: the y position in the image texture to start drawing from 
			imageX: the x position in the image texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def regionWidth(self, regionWidth: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			regionWidth: the width of the region to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRegionWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the region to draw. 
		"""
		pass

	@overload
	def regionHeight(self, regionHeight: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			regionHeight: the height of the region to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRegionHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the region to draw. 
		"""
		pass

	@overload
	def regionSize(self, regionWidth: int, regionHeight: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			regionHeight: the height of the region to draw 
			regionWidth: the width of the region to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def regions(self, x: int, y: int, width: int, height: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position in the image texture to start drawing from 
			width: the width of the region to draw 
			y: the y position in the image texture to start drawing from 
			height: the height of the region to draw 
		"""
		pass

	@overload
	def regions(self, x: int, y: int, width: int, height: int, textureWidth: int, textureHeight: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			textureWidth: the width of the used texture 
			x: the x position in the image texture to start drawing from 
			width: the width of the region to draw 
			y: the y position in the image texture to start drawing from 
			textureHeight: the height of the used texture 
			height: the height of the region to draw 
		"""
		pass

	@overload
	def textureWidth(self, textureWidth: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			textureWidth: the width of the used texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextureWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the used texture. 
		"""
		pass

	@overload
	def textureHeight(self, textureHeight: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			textureHeight: the height of the used texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextureHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the used texture. 
		"""
		pass

	@overload
	def textureSize(self, textureWidth: int, textureHeight: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			textureWidth: the width of the used texture 
			textureHeight: the height of the used texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, color: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def color(self, r: int, g: int, b: int) -> "Image_Builder":
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
	def color(self, r: int, g: int, b: int, a: int) -> "Image_Builder":
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
	def color(self, color: int, alpha: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			color: the color of the image 
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
			the color of the image. 
		"""
		pass

	@overload
	def alpha(self, alpha: int) -> "Image_Builder":
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
	def rotation(self, rotation: float) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the image in degrees 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the image in degrees. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Image_Builder":
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
	def zIndex(self, zIndex: int) -> "Image_Builder":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of the image 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the image. 
		"""
		pass

	@overload
	def createElement(self) -> Image:
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
	def moveTo(self, x: int, y: int) -> "Image_Builder":
		pass

	pass


