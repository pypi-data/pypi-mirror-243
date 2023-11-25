from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .RenderElement import RenderElement
from .Alignable import Alignable
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

B = TypeVar("B")
B = B

T = TypeVar("T")
net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class ClickableWidgetHelper(RenderElement, Alignable, Generic[B, T], BaseHelper):
	"""
	Since: 1.0.5 
	"""
	zIndex: int
	tooltips: List[Text]

	@overload
	def __init__(self, btn: T) -> None:
		pass

	@overload
	def __init__(self, btn: T, zIndex: int) -> None:
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.0.5 

		Returns:
			the 'x' coordinate of the button. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.0.5 

		Returns:
			the 'y' coordinate of the button. 
		"""
		pass

	@overload
	def setPos(self, x: int, y: int) -> B:
		"""Set the button position.\n
		Since: 1.0.5 

		Args:
			x: 
			y: 
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
			the height of the button. 
		"""
		pass

	@overload
	def setLabel(self, label: str) -> B:
		"""change the text.\n
		Since: 1.0.5, renamed from 'setText' in 1.3.1 

		Args:
			label: 
		"""
		pass

	@overload
	def setLabel(self, helper: TextHelper) -> B:
		"""change the text.\n
		Since: 1.3.1 

		Args:
			helper: 
		"""
		pass

	@overload
	def getLabel(self) -> TextHelper:
		"""
		Since: 1.2.3, renamed fro 'getText' in 1.3.1 

		Returns:
			current button text. 
		"""
		pass

	@overload
	def getActive(self) -> bool:
		"""
		Since: 1.0.5 

		Returns:
			button clickable state. 
		"""
		pass

	@overload
	def setActive(self, t: bool) -> B:
		"""set the button clickable state.\n
		Since: 1.0.5 

		Args:
			t: 
		"""
		pass

	@overload
	def setWidth(self, width: int) -> B:
		"""set the button width.\n
		Since: 1.0.5 

		Args:
			width: 
		"""
		pass

	@overload
	def click(self) -> B:
		"""clicks button\n
		Since: 1.3.1 
		"""
		pass

	@overload
	def click(self, await_: bool) -> B:
		"""clicks button\n
		Since: 1.3.1 

		Args:
			await: should wait for button to finish clicking. 
		"""
		pass

	@overload
	def setTooltip(self, tooltips: List[object]) -> B:
		"""
		Since: 1.8.4 

		Args:
			tooltips: the tooltips to set 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addTooltip(self, tooltip: object) -> B:
		"""
		Since: 1.8.4 

		Args:
			tooltip: the tooltips to add 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def removeTooltip(self, index: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			index: the index of the tooltip to remove 

		Returns:
			'true' if the tooltip was removed successfully, 'false' otherwise. 
		"""
		pass

	@overload
	def removeTooltip(self, tooltip: TextHelper) -> bool:
		"""
		Since: 1.8.4 

		Args:
			tooltip: the tooltip to remove 

		Returns:
			'true' if the tooltip was removed successfully, 'false' otherwise. 
		"""
		pass

	@overload
	def getTooltips(self) -> List[TextHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a copy of the tooltips. 
		"""
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def getZIndex(self) -> int:
		pass

	@overload
	def toString(self) -> str:
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


