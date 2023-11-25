from typing import overload
from typing import TypeVar
from .RenderElement import RenderElement
from .Alignable import Alignable
from .IDraw2D import IDraw2D
from .ItemStackHelper import ItemStackHelper

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack


class Item(RenderElement, Alignable):
	"""
	Since: 1.0.5 
	"""
	parent: IDraw2D
	item: ItemStack
	ovText: str
	overlay: bool
	scale: float
	rotation: float
	rotateCenter: bool
	x: int
	y: int
	zIndex: int

	@overload
	def __init__(self, x: int, y: int, zIndex: int, id: str, overlay: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, zIndex: int, i: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, zIndex: int, itemStack: ItemStackHelper, overlay: bool, scale: float, rotation: float, ovText: str) -> None:
		pass

	@overload
	def setItem(self, i: ItemStackHelper) -> "Item":
		"""
		Since: 1.0.5 [citation needed] 

		Args:
			i: 
		"""
		pass

	@overload
	def setItem(self, id: str, count: int) -> "Item":
		"""
		Since: 1.0.5 [citation needed] 

		Args:
			count: 
			id: 
		"""
		pass

	@overload
	def getItem(self) -> ItemStackHelper:
		"""
		Since: 1.0.5 [citation needed] 
		"""
		pass

	@overload
	def setX(self, x: int) -> "Item":
		"""
		Since: 1.8.4 

		Args:
			x: the new x position of this element 

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
	def setY(self, y: int) -> "Item":
		"""
		Since: 1.8.4 

		Args:
			y: the new y position of this element 

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
	def setPos(self, x: int, y: int) -> "Item":
		"""
		Since: 1.0.5 

		Args:
			x: 
			y: 
		"""
		pass

	@overload
	def setScale(self, scale: float) -> "Item":
		"""
		Since: 1.2.6 

		Args:
			scale: 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of this item. 
		"""
		pass

	@overload
	def setRotation(self, rotation: float) -> "Item":
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
			the rotation of this item. 
		"""
		pass

	@overload
	def setRotateCenter(self, rotateCenter: bool) -> "Item":
		"""
		Since: 1.8.4 

		Args:
			rotateCenter: whether the item should be rotated around its center 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isRotatingCenter(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this item should be rotated around its center, 'false' otherwise. 
		"""
		pass

	@overload
	def setOverlay(self, overlay: bool) -> "Item":
		"""
		Since: 1.2.0 

		Args:
			overlay: 
		"""
		pass

	@overload
	def shouldShowOverlay(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' , if the overlay, i.e. the durability bar, and the overlay text or
item count should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def setOverlayText(self, ovText: str) -> "Item":
		"""
		Since: 1.2.0 

		Args:
			ovText: 
		"""
		pass

	@overload
	def getOverlayText(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the overlay text of this item. 
		"""
		pass

	@overload
	def setZIndex(self, zIndex: int) -> "Item":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the new z-index of this item 

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
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float, is3dRender: bool) -> None:
		pass

	@overload
	def setParent(self, parent: IDraw2D) -> "Item":
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
	def moveTo(self, x: int, y: int) -> "Item":
		pass

	pass


