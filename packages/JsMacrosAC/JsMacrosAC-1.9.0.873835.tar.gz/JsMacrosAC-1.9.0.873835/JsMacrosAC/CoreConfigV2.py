from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .ScriptTrigger import ScriptTrigger
from .ServiceTrigger import ServiceTrigger

com_google_gson_JsonObject = TypeVar("com_google_gson_JsonObject")
JsonObject = com_google_gson_JsonObject


class CoreConfigV2:
	maxLockTime: float
	defaultProfile: str
	anythingIgnored: List[str]
	profiles: Mapping[str, List[ScriptTrigger]]
	services: Mapping[str, ServiceTrigger]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getCurrentProfile(self) -> str:
		pass

	@overload
	def setCurrentProfile(self, pname: str) -> None:
		pass

	@overload
	def profileOptions(self) -> List[str]:
		pass

	@overload
	def getEvents(self) -> List[str]:
		pass

	@overload
	def fromV1(self, v1: JsonObject) -> None:
		pass

	pass


