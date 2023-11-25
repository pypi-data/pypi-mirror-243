from typing import overload
from typing import TypeVar
from typing import Generic
from .ClickableWidgetHelper import ClickableWidgetHelper

T = TypeVar("T")

class ButtonWidgetHelper(Generic[T], ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: T) -> None:
		pass

	@overload
	def __init__(self, btn: T, zIndex: int) -> None:
		pass

	pass


