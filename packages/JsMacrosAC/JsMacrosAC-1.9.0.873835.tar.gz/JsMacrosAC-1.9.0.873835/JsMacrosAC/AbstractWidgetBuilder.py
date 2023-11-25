from typing import overload
from typing import TypeVar
from typing import Generic
from .Alignable import Alignable
from .TextHelper import TextHelper

B = TypeVar("B")
B = B

T = TypeVar("T")
U = TypeVar("U")

class AbstractWidgetBuilder(Alignable, Generic[B, T, U]):
	"""
	Since: 1.8.4 
	"""

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the widget. 
		"""
		pass

	@overload
	def width(self, width: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			width: the width of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the widget. 
		"""
		pass

	@overload
	def height(self, height: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			height: the height of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			width: the width of the widget 
			height: the height of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getZIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the z-index of the widget. 
		"""
		pass

	@overload
	def zIndex(self, zIndex: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			zIndex: the z-index of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position of the widget. 
		"""
		pass

	@overload
	def x(self, x: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position of the widget. 
		"""
		pass

	@overload
	def y(self, y: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			y: the y position of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def pos(self, x: int, y: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the widget 
			y: the y position of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMessage(self) -> TextHelper:
		"""
		Since: 1.8.4 

		Returns:
			the message of the widget or an empty text if none is set. 
		"""
		pass

	@overload
	def message(self, message: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			message: the message of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def message(self, message: TextHelper) -> B:
		"""
		Since: 1.8.4 

		Args:
			message: the message of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isActive(self) -> bool:
		"""An inactive widget can not be interacted with and may have a different appearance.\n
		Since: 1.8.4 

		Returns:
			'true' if the widget is active, 'false' otherwise. 
		"""
		pass

	@overload
	def active(self, active: bool) -> B:
		"""An inactive widget can not be interacted with and may have a different appearance.\n
		Since: 1.8.4 

		Args:
			active: whether the widget should be active or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isVisible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the widget is visible, 'false' otherwise. 
		"""
		pass

	@overload
	def visible(self, visible: bool) -> B:
		"""
		Since: 1.8.4 

		Args:
			visible: whether the widget should be visible or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAlpha(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the alpha value of the widget. 
		"""
		pass

	@overload
	def alpha(self, alpha: float) -> B:
		"""
		Since: 1.8.4 

		Args:
			alpha: the alpha value of the widget 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def build(self) -> U:
		"""
		Since: 1.8.4 

		Returns:
			the build widget for the set properties. 
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
	def moveTo(self, x: int, y: int) -> B:
		pass

	pass


