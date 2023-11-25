from typing import overload
from typing import List
from typing import TypeVar
from .IDraw2D import IDraw2D
from .MethodWrapper import MethodWrapper
from .Text import Text
from .Rect import Rect
from .Line import Line
from .Item import Item
from .Image import Image
from .Draw2DElement import Draw2DElement
from .RenderElement import RenderElement
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")
java_util_function_IntSupplier = TypeVar("java_util_function_IntSupplier")
IntSupplier = java_util_function_IntSupplier

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Draw2D(IDraw2D):
	"""
	Since: 1.0.5 
	"""
	widthSupplier: IntSupplier
	heightSupplier: IntSupplier
	zIndex: int
	visible: bool
	onInit: MethodWrapper
	catchInit: MethodWrapper

	@overload
	def __init__(self) -> None:
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
		Since: 1.0.5 
		"""
		pass

	@overload
	def getTexts(self) -> List[Text]:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def getRects(self) -> List[Rect]:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def getLines(self) -> List[Line]:
		pass

	@overload
	def getItems(self) -> List[Item]:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def getImages(self) -> List[Image]:
		"""
		Since: 1.2.3 
		"""
		pass

	@overload
	def getDraw2Ds(self) -> List[Draw2DElement]:
		pass

	@overload
	def getElements(self) -> List[RenderElement]:
		pass

	@overload
	def removeElement(self, e: RenderElement) -> "Draw2D":
		pass

	@overload
	def reAddElement(self, e: T) -> T:
		pass

	@overload
	def setVisible(self, visible: bool) -> "Draw2D":
		"""
		Since: 1.8.4 

		Args:
			visible: whether to render this element. 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isVisible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this draw2d is visible, 'false' otherwise. 
		"""
		pass

	@overload
	def addDraw2D(self, draw2D: "Draw2D", x: int, y: int, width: int, height: int) -> Draw2DElement:
		pass

	@overload
	def addDraw2D(self, draw2D: "Draw2D", x: int, y: int, width: int, height: int, zIndex: int) -> Draw2DElement:
		pass

	@overload
	def removeDraw2D(self, draw2D: Draw2DElement) -> "Draw2D":
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool) -> Text:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def removeText(self, t: Text) -> "Draw2D":
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		"""
		Since: 1.2.3 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.4.0 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, alpha: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def removeImage(self, i: Image) -> "Draw2D":
		"""
		Since: 1.2.3 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Rect:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int) -> Rect:
		"""
		Since: 1.1.8 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float) -> Rect:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float, zIndex: int) -> Rect:
		pass

	@overload
	def removeRect(self, r: Rect) -> "Draw2D":
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float, rotation: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float, rotation: float) -> Line:
		pass

	@overload
	def removeLine(self, l: Line) -> "Draw2D":
		pass

	@overload
	def addItem(self, x: int, y: int, id: str) -> Item:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool) -> Item:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, Item: ItemStackHelper) -> Item:
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, Item: ItemStackHelper, overlay: bool) -> Item:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def removeItem(self, i: Item) -> "Draw2D":
		"""
		Since: 1.0.5 
		"""
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext) -> None:
		pass

	@overload
	def getElementsByZIndex(self) -> iter:
		pass

	@overload
	def setOnInit(self, onInit: MethodWrapper) -> "Draw2D":
		"""init function, called when window is resized or screen/draw2d is registered.
clears all previous elements when called.\n
		Since: 1.2.7 

		Args:
			onInit: calls your method as a Consumer Draw2D 
		"""
		pass

	@overload
	def setOnFailInit(self, catchInit: MethodWrapper) -> "Draw2D":
		"""
		Since: 1.2.7 

		Args:
			catchInit: calls your method as a Consumer String 
		"""
		pass

	@overload
	def register(self) -> "Draw2D":
		"""register so the overlay actually renders\n
		Since: 1.6.5 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def unregister(self) -> "Draw2D":
		"""unregister so the overlay stops rendering\n
		Since: 1.6.5 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setZIndex(self, zIndex: int) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	pass


