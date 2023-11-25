from typing import overload
from typing import TypeVar

java_io_File = TypeVar("java_io_File")
File = java_io_File

java_util_Comparator_java_io_File_ = TypeVar("java_util_Comparator_java_io_File_")
Comparator = java_util_Comparator_java_io_File_


class FileChooser_sortFile(Comparator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, a: File, b: File) -> int:
		pass

	pass


