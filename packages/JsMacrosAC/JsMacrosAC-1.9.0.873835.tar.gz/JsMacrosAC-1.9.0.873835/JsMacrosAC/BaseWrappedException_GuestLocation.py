from typing import overload
from typing import TypeVar
from .BaseWrappedException_SourceLocation import BaseWrappedException_SourceLocation

java_io_File = TypeVar("java_io_File")
File = java_io_File


class BaseWrappedException_GuestLocation(BaseWrappedException_SourceLocation):
	file: File
	line: int
	column: int
	startIndex: int
	endIndex: int

	@overload
	def __init__(self, file: File, startIndex: int, endIndex: int, line: int, column: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


