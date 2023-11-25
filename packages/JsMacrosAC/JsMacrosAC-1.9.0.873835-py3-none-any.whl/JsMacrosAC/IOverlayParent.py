from typing import overload
from typing import TypeVar
from .IContainerParent import IContainerParent
from .OverlayContainer import OverlayContainer

net_minecraft_client_gui_Element = TypeVar("net_minecraft_client_gui_Element")
Element = net_minecraft_client_gui_Element


class IOverlayParent(IContainerParent):

	@overload
	def closeOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def setFocused(self, focused: Element) -> None:
		pass

	@overload
	def getChildOverlay(self) -> OverlayContainer:
		pass

	pass


