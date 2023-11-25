from typing import overload
from typing import TypeVar
from typing import Set
from .Core import Core
from .BaseEventRegistry import BaseEventRegistry
from .BaseEvent import BaseEvent

java_lang_Throwable = TypeVar("java_lang_Throwable")
Throwable = java_lang_Throwable

org_slf4j_Logger = TypeVar("org_slf4j_Logger")
Logger = org_slf4j_Logger

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class BaseProfile:
	"""
	Since: 1.2.7 
	"""
	LOGGER: Logger
	joinedThreadStack: Set[Thread]
	events: Set[str]
	profileName: str

	@overload
	def __init__(self, runner: Core, logger: Logger) -> None:
		pass

	@overload
	def logError(self, ex: Throwable) -> None:
		pass

	@overload
	def getRegistry(self) -> BaseEventRegistry:
		"""
		Since: 1.1.2 [citation needed] 
		"""
		pass

	@overload
	def checkJoinedThreadStack(self) -> bool:
		"""
		Since: 1.6.0 
		"""
		pass

	@overload
	def loadOrCreateProfile(self, profileName: str) -> None:
		"""
		Since: 1.1.2 [citation needed] 

		Args:
			profileName: 
		"""
		pass

	@overload
	def saveProfile(self) -> None:
		"""
		Since: 1.0.8 [citation needed] 
		"""
		pass

	@overload
	def triggerEvent(self, event: BaseEvent) -> None:
		"""
		Since: 1.2.7 

		Args:
			event: 
		"""
		pass

	@overload
	def init(self, defaultProfile: str) -> None:
		pass

	@overload
	def getCurrentProfileName(self) -> str:
		pass

	@overload
	def renameCurrentProfile(self, profile: str) -> None:
		pass

	pass


