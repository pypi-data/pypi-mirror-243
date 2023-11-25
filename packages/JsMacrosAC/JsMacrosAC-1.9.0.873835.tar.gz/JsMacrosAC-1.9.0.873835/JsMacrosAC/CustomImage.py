from typing import overload
from typing import List
from typing import Mapping


class CustomImage:
	"""
	Since: 1.8.4 
	"""
	IMAGES: Mapping[str, "CustomImage"]

	@overload
	def __init__(self, image: BufferedImage) -> None:
		pass

	@overload
	def __init__(self, image: BufferedImage, name: str) -> None:
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this image. 
		"""
		pass

	@overload
	def loadImage(self, path: str) -> BufferedImage:
		"""The image can be used with the drawImage methods to draw it onto this image.\n
		Since: 1.8.4 

		Args:
			path: the path to the image, relative to the jsMacros config folder 

		Returns:
			an image from the given path. 
		"""
		pass

	@overload
	def loadImage(self, path: str, x: int, y: int, width: int, height: int) -> BufferedImage:
		"""Loads the image from the given path and returns a subimage of it from the given positions.
The image can be used with the drawImage methods to draw it onto this image.\n
		Since: 1.8.4 

		Args:
			path: the path to the image, relative to the jsMacros config folder 
			x: the x position to get the subimage from 
			width: the width of the subimage 
			y: the y position to get the subimage from 
			height: the height of the subimage 

		Returns:
			the cropped image from the given path. 
		"""
		pass

	@overload
	def update(self) -> "CustomImage":
		"""Updates the texture to be drawn with the contents of this image. Any changes made to this
image will only be displayed after calling this method. The method must not be called after
each change, but rather when the image is finished being changed.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def saveImage(self, path: str, fileName: str) -> "CustomImage":
		"""Saves this image to the given path. The file will be saved as a png.\n
		Since: 1.8.4 

		Args:
			path: the path to the image, relative to the jsMacros config folder 
			fileName: the file name of the image, without the extension 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getIdentifier(self) -> str:
		"""The identifier should be used with any buttons and textures in the draw2D and other classes,
which require an identifier.\n
		Since: 1.8.4 

		Returns:
			the identifier of this image. 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""The width is a constant and will not change.\n
		Since: 1.8.4 

		Returns:
			the width of this image. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""The height is a constant and will not change.\n
		Since: 1.8.4 

		Returns:
			the height of this image. 
		"""
		pass

	@overload
	def getImage(self) -> BufferedImage:
		"""
		Since: 1.8.4 

		Returns:
			the internal BufferedImage of this image, which all updates are made to. 
		"""
		pass

	@overload
	def getPixel(self, x: int, y: int) -> int:
		"""The color is in the ARGB format.\n
		Since: 1.8.4 

		Args:
			x: the x position to get the color from 
			y: the y position to get the color from 

		Returns:
			the color at the given position. 
		"""
		pass

	@overload
	def setPixel(self, x: int, y: int, argb: int) -> "CustomImage":
		"""The color is in the ARGB format.\n
		Since: 1.8.4 

		Args:
			argb: the ARGB value to set the pixel to 
			x: the x position to set the color at 
			y: the y position to set the color at 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawImage(self, img: Image, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			img: the image to draw onto this image 
			x: the x position to draw the image at 
			width: the width of the image to draw 
			y: the y position to draw the image at 
			height: the height of the image to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawImage(self, img: Image, x: int, y: int, width: int, height: int, sourceX: int, sourceY: int, sourceWidth: int, sourceHeight: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			sourceX: the x position of the subimage to draw 
			img: the image to draw onto this image 
			sourceY: the y position of the subimage to draw 
			sourceWidth: the width of the subimage to draw 
			x: the x position to draw the image at 
			width: the width of the image to draw 
			y: the y position to draw the image at 
			sourceHeight: the height of the subimage to draw 
			height: the height of the image to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getGraphicsColor(self) -> int:
		"""The color is a rgb value which is used for draw and fill operations.\n
		Since: 1.8.4 

		Returns:
			the graphics current rgb color. 
		"""
		pass

	@overload
	def setGraphicsColor(self, color: int) -> "CustomImage":
		"""The color is a rgb value which is used for draw and fill operations.\n
		Since: 1.8.4 

		Args:
			color: the rgb color to use for graphics operations 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def translate(self, x: int, y: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the origin point 
			y: the y position of the origin point 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clipRect(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""

		Args:
			x: the x coordinate of the rectangle to intersect the clip with 
			width: the width of the rectangle to intersect the clip with 
			y: the y coordinate of the rectangle to intersect the clip with 
			height: the height of the rectangle to intersect the clip with 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setClip(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the new clip rectangle 
			width: the width of the new clip rectangle 
			y: the y coordinate of the new clip rectangle 
			height: the height of the new clip rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setPaintMode(self) -> "CustomImage":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setXorMode(self, color: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			color: the color to use for the xor operation 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getClipBounds(self) -> Rectangle:
		"""
		Since: 1.8.4 

		Returns:
			an array with the bounds of the current clip. 
		"""
		pass

	@overload
	def copyArea(self, x: int, y: int, width: int, height: int, dx: int, dy: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			dx: the offset to the x position to copy to 
			dy: the offset to the y position to copy to 
			x: the x position to copy from 
			width: the width of the area to copy 
			y: the y position to copy from 
			height: the height of the area to copy 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawLine(self, x1: int, y1: int, x2: int, y2: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			y1: the first y position of the line 
			x1: the first x position of the line 
			y2: the second y position of the line 
			x2: the second x position of the line 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawRect(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the rectangle 
			width: the width of the rectangle 
			y: the y position of the rectangle 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillRect(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the rectangle 
			width: the width of the rectangle 
			y: the y position of the rectangle 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clearRect(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the rectangle 
			width: the width of the rectangle 
			y: the y position of the rectangle 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clearRect(self, x: int, y: int, width: int, height: int, color: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			color: the rgb color to fill the rectangle with 
			x: the x position of the rectangle 
			width: the width of the rectangle 
			y: the y position of the rectangle 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawRoundRect(self, x: int, y: int, width: int, height: int, arcWidth: int, arcHeight: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			arcHeight: the vertical diameter of the arc at the four corners 
			arcWidth: the horizontal diameter of the arc at the four corners 
			x: the x position to draw the rectangle at 
			width: the width of the rectangle 
			y: the y position to draw the rectangle at 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillRoundRect(self, x: int, y: int, width: int, height: int, arcWidth: int, arcHeight: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			arcHeight: the vertical diameter of the arc at the four corners 
			arcWidth: the horizontal diameter of the arc at the four corners 
			x: the x position to draw the rectangle at 
			width: the width of the rectangle 
			y: the y position to draw the rectangle at 
			height: the height of the rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def draw3DRect(self, x: int, y: int, width: int, height: int, raised: bool) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position to draw the 3D rectangle at 
			width: the width of the 3D rectangle 
			raised: whether the rectangle should be raised above the surface or etched into the
              surface 
			y: the y position to draw the 3D rectangle at 
			height: the height of the 3D rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fill3DRect(self, x: int, y: int, width: int, height: int, raised: bool) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position to draw the 3D rectangle at 
			width: the width of the 3D rectangle 
			raised: whether the rectangle should be raised above the surface or etched into the
              surface 
			y: the y position to draw the 3D rectangle at 
			height: the height of the 3D rectangle 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawOval(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position to draw the oval at 
			width: the width of the oval 
			y: the y position to draw the oval at 
			height: the height of the oval 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillOval(self, x: int, y: int, width: int, height: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position to draw the oval at 
			width: the width of the oval 
			y: the y position to draw the oval at 
			height: the height of the oval 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawArc(self, x: int, y: int, width: int, height: int, startAngle: int, arcAngle: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			startAngle: the beginning angle 
			x: the x position to draw the arc at 
			width: the width of the arc 
			y: the y position to draw the arc at 
			arcAngle: the angular extent of the arc, relative to the start angle 
			height: the height of the arc 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillArc(self, x: int, y: int, width: int, height: int, startAngle: int, arcAngle: int) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			startAngle: the beginning angle 
			x: the x position to draw the arc at 
			width: the width of the arc 
			y: the y position to draw the arc at 
			arcAngle: the angular extent of the arc, relative to the start angle 
			height: the height of the arc 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawPolygonLine(self, pointsX: List[int], pointsY: List[int]) -> "CustomImage":
		"""The x and y array must have the same length and order for the points.\n
		Since: 1.8.4 

		Args:
			pointsY: an array of all y positions of the points in the polygon 
			pointsX: an array of all x positions of the points in the polygon 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawPolygon(self, pointsX: List[int], pointsY: List[int]) -> "CustomImage":
		"""The x and y array must have the same length and order for the points.\n
		Since: 1.8.4 

		Args:
			pointsY: an array of all y positions of the points in the polygon 
			pointsX: an array of all x positions of the points in the polygon 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def fillPolygon(self, pointsX: List[int], pointsY: List[int]) -> "CustomImage":
		"""The x and y array must have the same length and order for the points.\n
		Since: 1.8.4 

		Args:
			pointsY: an array of all y positions of the points in the polygon 
			pointsX: an array of all x positions of the points in the polygon 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def drawString(self, x: int, y: int, text: str) -> "CustomImage":
		"""
		Since: 1.8.4 

		Args:
			x: the x position to draw the string at 
			y: the y position to draw the string at 
			text: the text to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getStringWidth(self, toAnalyze: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			toAnalyze: the string to analyze 

		Returns:
			the width of the string for the current font in pixels 
		"""
		pass

	@overload
	def createWidget(self, width: int, height: int, name: str) -> "CustomImage":
		pass

	@overload
	def createWidget(self, path: str, name: str) -> "CustomImage":
		pass

	@overload
	def nativeARGBFlip(self, argb: int) -> int:
		"""Minecraft textures use an ABGR format for some reason.\n
		Since: 1.8.4 

		Args:
			argb: the argb color to transform 

		Returns:
			the abgr argb for the given argb color. 
		"""
		pass

	pass


