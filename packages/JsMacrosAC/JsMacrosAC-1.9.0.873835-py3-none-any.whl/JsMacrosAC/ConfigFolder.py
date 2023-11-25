from typing import overload
from typing import TypeVar

java_io_File = TypeVar("java_io_File")
File = java_io_File


class ConfigFolder:

	@overload
	def getFolder(self) -> File:
		pass

	pass


