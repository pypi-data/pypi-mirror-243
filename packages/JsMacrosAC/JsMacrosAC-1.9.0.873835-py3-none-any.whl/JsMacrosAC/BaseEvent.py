from typing import overload
from .BaseProfile import BaseProfile


class BaseEvent:
	profile: BaseProfile

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def cancellable(self) -> bool:
		pass

	@overload
	def joinable(self) -> bool:
		pass

	@overload
	def cancel(self) -> None:
		pass

	@overload
	def isCanceled(self) -> bool:
		pass

	@overload
	def getEventName(self) -> str:
		pass

	@overload
	def trigger(self) -> None:
		pass

	pass


