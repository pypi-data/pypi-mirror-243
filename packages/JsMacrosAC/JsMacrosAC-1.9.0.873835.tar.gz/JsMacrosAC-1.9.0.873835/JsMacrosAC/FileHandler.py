from typing import overload
from typing import List
from typing import TypeVar
from .FileHandler_FileLineIterator import FileHandler_FileLineIterator

java_io_BufferedInputStream = TypeVar("java_io_BufferedInputStream")
BufferedInputStream = java_io_BufferedInputStream

java_io_File = TypeVar("java_io_File")
File = java_io_File


class FileHandler:
	"""
	Since: 1.1.8 
	"""

	@overload
	def __init__(self, path: str) -> None:
		pass

	@overload
	def __init__(self, path: str, charset: str) -> None:
		pass

	@overload
	def __init__(self, path: File, charset: str) -> None:
		pass

	@overload
	def __init__(self, path: str, charset: Charset) -> None:
		pass

	@overload
	def __init__(self, path: File) -> None:
		pass

	@overload
	def __init__(self, path: File, charset: Charset) -> None:
		pass

	@overload
	def write(self, s: str) -> "FileHandler":
		"""writes a string to the file. this is a destructive operation that replaces the file contents.\n
		Since: 1.1.8 

		Args:
			s: 

		Returns:
			self 
		"""
		pass

	@overload
	def write(self, b: List[float]) -> "FileHandler":
		"""writes a byte array to the file. this is a destructive operation that replaces the file contents.\n
		Since: 1.1.8 

		Args:
			b: 

		Returns:
			self 
		"""
		pass

	@overload
	def read(self) -> str:
		"""
		Since: 1.1.8 
		"""
		pass

	@overload
	def readBytes(self) -> List[float]:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def readLines(self) -> FileHandler_FileLineIterator:
		"""get an iterator for the lines in the file.
please call FileHandler_FileLineIterator#close() when you are done with the iterator to not leak resources.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def streamBytes(self) -> BufferedInputStream:
		"""get an input stream for the file.
please call BufferedInputStream#close() when you are done with the stream to not leak resources.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def append(self, s: str) -> "FileHandler":
		"""
		Since: 1.1.8 

		Args:
			s: 

		Returns:
			self 
		"""
		pass

	@overload
	def append(self, b: List[float]) -> "FileHandler":
		"""
		Since: 1.2.6 

		Args:
			b: 

		Returns:
			self 
		"""
		pass

	@overload
	def getFile(self) -> File:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


