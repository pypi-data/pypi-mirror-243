from typing import overload
from typing import List
from typing import TypeVar
from .BaseProfile import BaseProfile
from .Core import Core

java_lang_Throwable = TypeVar("java_lang_Throwable")
Throwable = java_lang_Throwable

org_slf4j_Logger = TypeVar("org_slf4j_Logger")
Logger = org_slf4j_Logger


class Profile(BaseProfile):
	ignoredErrors: List[Class]

	@overload
	def __init__(self, runner: Core, logger: Logger) -> None:
		pass

	@overload
	def logError(self, ex: Throwable) -> None:
		pass

	@overload
	def checkJoinedThreadStack(self) -> bool:
		pass

	@overload
	def initRegistries(self) -> None:
		pass

	pass


