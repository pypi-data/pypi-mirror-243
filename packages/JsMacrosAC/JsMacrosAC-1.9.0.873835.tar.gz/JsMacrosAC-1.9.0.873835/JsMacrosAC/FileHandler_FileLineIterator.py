from typing import overload
from typing import TypeVar

java_io_File = TypeVar("java_io_File")
File = java_io_File


class FileHandler_FileLineIterator(iter, AutoCloseable):

	@overload
	def __init__(self, file: File, charset: Charset) -> None:
		pass

	@overload
	def hasNext(self) -> bool:
		pass

	@overload
	def next(self) -> str:
		pass

	@overload
	def close(self) -> None:
		pass

	pass


