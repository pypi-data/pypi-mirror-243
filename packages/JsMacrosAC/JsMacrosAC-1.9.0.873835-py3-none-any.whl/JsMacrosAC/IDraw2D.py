from typing import overload
from typing import List
from typing import TypeVar
from .Text import Text
from .Rect import Rect
from .Line import Line
from .Item import Item
from .Image import Image
from .Draw2DElement import Draw2DElement
from .RenderElement import RenderElement
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper
from .Draw2D import Draw2D
from .Item_Builder import Item_Builder
from .Image_Builder import Image_Builder
from .Rect_Builder import Rect_Builder
from .Line_Builder import Line_Builder
from .Text_Builder import Text_Builder
from .Draw2DElement_Builder import Draw2DElement_Builder
from .MethodWrapper import MethodWrapper

T = TypeVar("T")
net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class IDraw2D:
	"""
	Since: 1.2.7 
	"""

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.2.7 

		Returns:
			screen width 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.2.7 

		Returns:
			screen height 
		"""
		pass

	@overload
	def getTexts(self) -> List[Text]:
		"""
		Since: 1.2.7 

		Returns:
			text elements 
		"""
		pass

	@overload
	def getRects(self) -> List[Rect]:
		"""
		Since: 1.2.7 

		Returns:
			rect elements 
		"""
		pass

	@overload
	def getLines(self) -> List[Line]:
		"""
		Since: 1.8.4 

		Returns:
			all registered line elements. 
		"""
		pass

	@overload
	def getItems(self) -> List[Item]:
		"""
		Since: 1.2.7 

		Returns:
			item elements 
		"""
		pass

	@overload
	def getImages(self) -> List[Image]:
		"""
		Since: 1.2.7 

		Returns:
			image elements 
		"""
		pass

	@overload
	def getDraw2Ds(self) -> List[Draw2DElement]:
		"""
		Since: 1.8.4 

		Returns:
			all registered draw2d elements. 
		"""
		pass

	@overload
	def getElements(self) -> List[RenderElement]:
		"""
		Since: 1.2.9 

		Returns:
			a read only copy of the list of all elements added by scripts. 
		"""
		pass

	@overload
	def removeElement(self, e: RenderElement) -> T:
		"""removes any element regardless of type.\n
		Since: 1.2.9 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def reAddElement(self, e: T) -> T:
		"""re-add an element you removed with IDraw2D#removeElement(xyz.wagyourtail.jsmacros.client.api.classes.render.components.RenderElement)\n
		Since: 1.2.9 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool) -> Text:
		"""
		Since: 1.2.7 

		Args:
			color: text color 
			shadow: include shadow layer 
			x: screen x 
			y: screen y 
			text: 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		"""
		Since: 1.4.0 

		Args:
			color: text color 
			shadow: include shadow layer 
			x: screen x 
			y: screen y 
			text: 
			zIndex: z-index 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		"""
		Since: 1.2.7 

		Args:
			color: text color 
			shadow: include shadow layer 
			rotation: text rotation (as degrees) 
			x: screen x 
			y: screen y 
			scale: text scale (as double) 
			text: 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		"""
		Since: 1.4.0 

		Args:
			color: text color 
			shadow: include shadow layer 
			rotation: text rotation (as degrees) 
			x: screen x 
			y: screen y 
			scale: text scale (as double) 
			text: 
			zIndex: z-index 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool) -> Text:
		"""
		Since: 1.2.7 

		Args:
			color: text color 
			shadow: include shadow layer 
			x: screen x 
			y: screen y 
			text: 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		"""
		Since: 1.4.0 

		Args:
			color: text color 
			shadow: include shadow layer 
			x: screen x 
			y: screen y 
			text: 
			zIndex: z-index 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		"""
		Since: 1.2.7 

		Args:
			color: text color 
			shadow: include shadow layer 
			rotation: text rotation (as degrees) 
			x: screen x 
			y: screen y 
			scale: text scale (as double) 
			text: 

		Returns:
			added text 
		"""
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		"""
		Since: 1.4.0 

		Args:
			color: text color 
			shadow: include shadow layer 
			rotation: text rotation (as degrees) 
			x: screen x 
			y: screen y 
			scale: text scale (as double) 
			text: 
			zIndex: z-index 

		Returns:
			added text 
		"""
		pass

	@overload
	def removeText(self, t: Text) -> T:
		"""
		Since: 1.2.7 

		Args:
			t: 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		"""
		Since: 1.2.7 

		Args:
			imageY: the top-most coordinate of the texture region 
			textureWidth: the width of the entire texture 
			imageX: the left-most coordinate of the texture region 
			x: screen x, top left corner 
			width: width on screen 
			y: screen y, top left corner 
			regionHeight: the height the texture region 
			id: image id, in the form 'minecraft:textures' path'd as found in texture packs, ie 'assets/minecraft/textures/gui/recipe_book.png' becomes 'minecraft:textures/gui/recipe_book.png' 
			regionWidth: the width the texture region 
			textureHeight: the height of the entire texture 
			height: height on screen 

		Returns:
			added image 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		"""
		Since: 1.4.0 

		Args:
			imageY: the top-most coordinate of the texture region 
			textureWidth: the width of the entire texture 
			imageX: the left-most coordinate of the texture region 
			x: screen x, top left corner 
			width: width on screen 
			y: screen y, top left corner 
			regionHeight: the height the texture region 
			id: image id, in the form 'minecraft:textures' path'd as found in texture packs, ie 'assets/minecraft/textures/gui/recipe_book.png' becomes 'minecraft:textures/gui/recipe_book.png' 
			regionWidth: the width the texture region 
			textureHeight: the height of the entire texture 
			height: height on screen 
			zIndex: z-index 

		Returns:
			added image 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.2.7 

		Args:
			imageY: the top-most coordinate of the texture region 
			textureWidth: the width of the entire texture 
			imageX: the left-most coordinate of the texture region 
			rotation: the rotation (clockwise) of the texture (as degrees) 
			x: screen x, top left corner 
			width: width on screen 
			y: screen y, top left corner 
			regionHeight: the height the texture region 
			id: image id, in the form 'minecraft:textures' path'd as found in texture packs, ie 'assets/minecraft/textures/gui/recipe_book.png' becomes 'minecraft:textures/gui/recipe_book.png' 
			regionWidth: the width the texture region 
			textureHeight: the height of the entire texture 
			height: height on screen 

		Returns:
			added image 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.4.0 

		Args:
			imageY: the top-most coordinate of the texture region 
			textureWidth: the width of the entire texture 
			imageX: the left-most coordinate of the texture region 
			rotation: the rotation (clockwise) of the texture (as degrees) 
			regionWidth: the width the texture region 
			textureHeight: the height of the entire texture 
			x: screen x, top left corner 
			width: width on screen 
			y: screen y, top left corner 
			regionHeight: the height the texture region 
			id: image id, in the form 'minecraft:textures' path'd as found in texture packs, ie 'assets/minecraft/textures/gui/recipe_book.png' becomes 'minecraft:textures/gui/recipe_book.png' 
			height: height on screen 
			zIndex: z-index 

		Returns:
			added image 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 

		Args:
			color: 
			imageY: 
			textureWidth: 
			imageX: 
			rotation: 
			regionWidth: 
			textureHeight: 
			x: 
			width: 
			y: 
			regionHeight: 
			id: 
			height: 
			zIndex: 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, alpha: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 

		Args:
			color: 
			imageY: 
			textureWidth: 
			imageX: 
			rotation: 
			regionWidth: 
			textureHeight: 
			alpha: 
			x: 
			width: 
			y: 
			regionHeight: 
			id: 
			height: 
			zIndex: 
		"""
		pass

	@overload
	def removeImage(self, i: Image) -> T:
		"""
		Since: 1.2.7 

		Args:
			i: 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Rect:
		"""
		Since: 1.2.7 

		Args:
			color: as hex, with alpha channel 
			y1: 
			x1: 
			y2: 
			x2: 

		Returns:
			added rect 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int) -> Rect:
		"""
		Since: 1.2.7 

		Args:
			color: as hex 
			alpha: alpha channel 0-255 
			y1: 
			x1: 
			y2: 
			x2: 

		Returns:
			added rect 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float) -> Rect:
		"""
		Since: 1.2.7 

		Args:
			color: as hex 
			alpha: alpha channel 0-255 
			rotation: as degrees 
			y1: 
			x1: 
			y2: 
			x2: 

		Returns:
			added rect 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float, zIndex: int) -> Rect:
		"""
		Since: 1.4.0 

		Args:
			color: as hex 
			alpha: alpha channel 0-255 
			rotation: as degrees 
			y1: 
			x1: 
			y2: 
			x2: 
			zIndex: z-index 

		Returns:
			added rect 
		"""
		pass

	@overload
	def removeRect(self, r: Rect) -> T:
		"""
		Since: 1.2.7 

		Args:
			r: 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			y1: the y position of the start 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			y1: the y position of the start 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 
			zIndex: the z-index of the line 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			y1: the y position of the start 
			width: the width of the line 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			y1: the y position of the start 
			width: the width of the line 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 
			zIndex: the z-index of the line 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float, rotation: float) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			rotation: the rotation (clockwise) of the line (as degrees) 
			y1: the y position of the start 
			width: the width of the line 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float, rotation: float) -> Line:
		"""
		Since: 1.8.4 

		Args:
			color: the color of the line, can include alpha value 
			rotation: the rotation (clockwise) of the line (as degrees) 
			y1: the y position of the start 
			width: the width of the line 
			x1: the x position of the start 
			y2: the y position of the end 
			x2: the x position of the end 
			zIndex: the z-index of the line 

		Returns:
			the added line. 
		"""
		pass

	@overload
	def removeLine(self, l: Line) -> T:
		"""
		Since: 1.8.4 

		Args:
			l: the line to remove 

		Returns:
			self chaining. 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, id: str) -> Item:
		"""
		Since: 1.2.7 

		Args:
			x: left most corner 
			y: top most corner 
			id: item id 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str) -> Item:
		"""
		Since: 1.4.0 

		Args:
			x: left most corner 
			y: top most corner 
			id: item id 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool) -> Item:
		"""
		Since: 1.2.7 

		Args:
			overlay: should include overlay health and count 
			x: left most corner 
			y: top most corner 
			id: item id 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool) -> Item:
		"""
		Since: 1.4.0 

		Args:
			overlay: should include overlay health and count 
			x: left most corner 
			y: top most corner 
			id: item id 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.2.7 

		Args:
			overlay: should include overlay health and count 
			rotation: rotation of item 
			x: left most corner 
			y: top most corner 
			scale: scale of item 
			id: item id 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.4.0 

		Args:
			overlay: should include overlay health and count 
			rotation: rotation of item 
			x: left most corner 
			y: top most corner 
			scale: scale of item 
			id: item id 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper) -> Item:
		"""
		Since: 1.2.7 

		Args:
			item: from inventory as helper 
			x: left most corner 
			y: top most corner 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper) -> Item:
		"""
		Since: 1.4.0 

		Args:
			item: from inventory as helper 
			x: left most corner 
			y: top most corner 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool) -> Item:
		"""
		Since: 1.2.7 

		Args:
			item: from inventory as helper 
			overlay: should include overlay health and count 
			x: left most corner 
			y: top most corner 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool) -> Item:
		"""
		Since: 1.4.0 

		Args:
			item: from inventory as helper 
			overlay: should include overlay health and count 
			x: left most corner 
			y: top most corner 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.2.7 

		Args:
			item: from inventory as helper 
			overlay: should include overlay health and count 
			rotation: rotation of item 
			x: left most corner 
			y: top most corner 
			scale: scale of item 

		Returns:
			added item 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.4.0 

		Args:
			item: from inventory as helper 
			overlay: should include overlay health and count 
			rotation: rotation of item 
			x: left most corner 
			y: top most corner 
			scale: scale of item 
			zIndex: z-index 

		Returns:
			added item 
		"""
		pass

	@overload
	def removeItem(self, i: Item) -> T:
		"""
		Since: 1.2.7 

		Args:
			i: 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addDraw2D(self, draw2D: Draw2D, x: int, y: int, width: int, height: int) -> Draw2DElement:
		"""Tries to add the given draw2d as a child. Fails if cyclic dependencies are detected.\n
		Since: 1.8.4 

		Args:
			x: the x position on this draw2d 
			width: the width of the given draw2d 
			y: the y position on this draw2d 
			draw2D: the draw2d to add 
			height: the height of the given draw2d 

		Returns:
			a wrapper for the draw2d. 
		"""
		pass

	@overload
	def addDraw2D(self, draw2D: Draw2D, x: int, y: int, width: int, height: int, zIndex: int) -> Draw2DElement:
		"""Tries to add the given draw2d as a child. Fails if cyclic dependencies are detected.\n
		Since: 1.8.4 

		Args:
			x: the x position on this draw2d 
			width: the width of the given draw2d 
			y: the y position on this draw2d 
			draw2D: the draw2d to add 
			height: the height of the given draw2d 
			zIndex: the z-index for the draw2d 

		Returns:
			a wrapper for the draw2d. 
		"""
		pass

	@overload
	def removeDraw2D(self, draw2D: Draw2DElement) -> T:
		"""
		Since: 1.8.4 

		Args:
			draw2D: the draw2d to remove 

		Returns:
			self chaining. 
		"""
		pass

	@overload
	def itemBuilder(self) -> Item_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a builder for an Item . 
		"""
		pass

	@overload
	def itemBuilder(self, item: ItemStackHelper) -> Item_Builder:
		"""
		Since: 1.8.4 

		Args:
			item: the item to use 

		Returns:
			a builder for an Item . 
		"""
		pass

	@overload
	def imageBuilder(self) -> Image_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a builder for an Image . 
		"""
		pass

	@overload
	def imageBuilder(self, id: str) -> Image_Builder:
		"""
		Since: 1.8.4 

		Args:
			id: the id of the image 

		Returns:
			a builder for an Image . 
		"""
		pass

	@overload
	def rectBuilder(self) -> Rect_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a builder for a Rect . 
		"""
		pass

	@overload
	def rectBuilder(self, x: int, y: int, width: int, height: int) -> Rect_Builder:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the rectangle 
			width: the width of the rectangle 
			y: the y position of the rectangle 
			height: the height of the rectangle 

		Returns:
			a builder for a Rect . 
		"""
		pass

	@overload
	def lineBuilder(self) -> Line_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a builder for a Line . 
		"""
		pass

	@overload
	def lineBuilder(self, x1: int, y1: int, x2: int, y2: int) -> Line_Builder:
		"""
		Since: 1.8.4 

		Args:
			y1: the y position of the first point 
			x1: the x position of the first point 
			y2: the y position of the second point 
			x2: the x position of the second point 

		Returns:
			a builder for a Line . 
		"""
		pass

	@overload
	def textBuilder(self) -> Text_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a builder for a Text . 
		"""
		pass

	@overload
	def textBuilder(self, text: str) -> Text_Builder:
		"""
		Since: 1.8.4 

		Args:
			text: the text to display 

		Returns:
			a builder for a Text . 
		"""
		pass

	@overload
	def textBuilder(self, text: TextHelper) -> Text_Builder:
		"""
		Since: 1.8.4 

		Args:
			text: the text to display 

		Returns:
			a builder for a Text . 
		"""
		pass

	@overload
	def draw2DBuilder(self, draw2D: Draw2D) -> Draw2DElement_Builder:
		"""
		Since: 1.8.4 

		Args:
			draw2D: the draw2d to add 

		Returns:
			a builder for a Draw2D . 
		"""
		pass

	@overload
	def setOnInit(self, onInit: MethodWrapper) -> T:
		"""
		Since: 1.2.7 

		Args:
			onInit: calls your method as a Consumer IDraw2D#T 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setOnFailInit(self, catchInit: MethodWrapper) -> T:
		"""
		Since: 1.2.7 

		Args:
			catchInit: calls your method as a Consumer String 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def render(self, drawContext: DrawContext) -> None:
		"""internal

		Args:
			drawContext: 
		"""
		pass

	@overload
	def setZIndex(self, zIndex: int) -> None:
		"""
		Since: 1.8.4 

		Args:
			zIndex: 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 
		"""
		pass

	pass


