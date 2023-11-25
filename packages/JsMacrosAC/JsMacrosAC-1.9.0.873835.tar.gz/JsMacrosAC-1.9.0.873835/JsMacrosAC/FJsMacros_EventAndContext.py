from typing import overload
from typing import TypeVar
from typing import Generic
from .EventContainer import EventContainer

E = TypeVar("E")
E = E


class FJsMacros_EventAndContext(Generic[E]):
	event: E
	context: EventContainer

	@overload
	def __init__(self, event: E, context: EventContainer) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


