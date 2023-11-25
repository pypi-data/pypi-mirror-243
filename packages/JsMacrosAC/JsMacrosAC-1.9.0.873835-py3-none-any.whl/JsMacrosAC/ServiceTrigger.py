from typing import overload
from typing import TypeVar
from .ScriptTrigger import ScriptTrigger

java_io_File = TypeVar("java_io_File")
File = java_io_File


class ServiceTrigger:
	file: str
	enabled: bool

	@overload
	def __init__(self, file: File, enabled: bool) -> None:
		pass

	@overload
	def toScriptTrigger(self) -> ScriptTrigger:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	pass


