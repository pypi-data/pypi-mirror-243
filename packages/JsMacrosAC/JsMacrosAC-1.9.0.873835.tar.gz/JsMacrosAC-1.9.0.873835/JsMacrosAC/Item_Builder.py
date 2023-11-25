from typing import overload
from .Alignable import Alignable
from .RenderElementBuilder import RenderElementBuilder
from .IDraw2D import IDraw2D
from .ItemStackHelper import ItemStackHelper


class Item_Builder(Alignable, RenderElementBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, draw2D: IDraw2D) -> None:
		pass

	@overload
	def x(self, x: int) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the item. 
		"""
		pass

	@overload
	def y(self, y: int) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			y: the y position of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the item. 
		"""
		pass

	@overload
	def pos(self, x: int, y: int) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the item 
			y: the y position of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def item(self, item: ItemStackHelper) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			item: the item to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def item(self, id: str) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			id: the id of the item to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def item(self, id: str, count: int) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			count: the stack size 
			id: the id of the item to draw 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getItem(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item to be drawn. 
		"""
		pass

	@overload
	def overlayText(self, overlayText: str) -> "Item_Builder":
		"""This also sets the overlay to be shown.\n
		Since: 1.8.4 

		Args:
			overlayText: the overlay text 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getOverlayText(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the overlay text. 
		"""
		pass

	@overload
	def overlayVisible(self, visible: bool) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			visible: whether the overlay should be visible or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isOverlayVisible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the overlay should be visible, 'false' otherwise. 
		"""
		pass

	@overload
	def scale(self, scale: float) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			scale: the scale of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getScale(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the scale of the item. 
		"""
		pass

	@overload
	def rotation(self, rotation: float) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			rotation: the rotation (clockwise) of the item in degrees 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRotation(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the rotation (clockwise) of the item in degrees. 
		"""
		pass

	@overload
	def rotateCenter(self, rotateCenter: bool) -> "Item_Builder":
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
	def zIndex(self, zIndex: int) -> "Item_Builder":
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of the item 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the item. 
		"""
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
	def moveTo(self, x: int, y: int) -> "Item_Builder":
		pass

	pass


