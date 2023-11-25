from typing import overload
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent

T = TypeVar("T")
net_minecraft_client_gui_Element = TypeVar("net_minecraft_client_gui_Element")
Element = net_minecraft_client_gui_Element


class IContainerParent:

	@overload
	def addDrawableChild(self, drawableElement: T) -> T:
		pass

	@overload
	def remove(self, button: Element) -> None:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer, disableButtons: bool) -> None:
		pass

	@overload
	def getFirstOverlayParent(self) -> IOverlayParent:
		pass

	pass


