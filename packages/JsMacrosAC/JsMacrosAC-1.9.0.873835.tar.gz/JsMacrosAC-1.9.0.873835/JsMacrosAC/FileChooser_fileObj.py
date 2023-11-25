from typing import overload
from typing import TypeVar
from .Button import Button

java_io_File = TypeVar("java_io_File")
File = java_io_File


class FileChooser_fileObj:
	file: File
	btn: Button

	@overload
	def __init__(self, file: File, btn: Button) -> None:
		pass

	pass


