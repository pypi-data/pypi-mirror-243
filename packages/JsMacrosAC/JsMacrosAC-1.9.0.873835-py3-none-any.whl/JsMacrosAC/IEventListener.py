from typing import overload
from .BaseEvent import BaseEvent
from .EventContainer import EventContainer


class IEventListener:
	NULL: "IEventListener"

	@overload
	def joined(self) -> bool:
		pass

	@overload
	def trigger(self, event: BaseEvent) -> EventContainer:
		pass

	@overload
	def off(self) -> None:
		"""Used for self unregistering events.\n
		Since: 1.8.4 
		"""
		pass

	pass


