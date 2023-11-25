from typing import overload
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent
from .FileChooser_fileObj import FileChooser_fileObj

java_util_function_Consumer_java_io_File_ = TypeVar("java_util_function_Consumer_java_io_File_")
Consumer = java_util_function_Consumer_java_io_File_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

java_io_File = TypeVar("java_io_File")
File = java_io_File

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class FileChooser(OverlayContainer):
	root: File

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, directory: File, selected: File, parent: IOverlayParent, setFile: Consumer, editFile: Consumer) -> None:
		pass

	@overload
	def setDir(self, dir: File) -> None:
		pass

	@overload
	def selectFile(self, f: File) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def addFile(self, f: File) -> None:
		pass

	@overload
	def addFile(self, f: File, btnText: str) -> None:
		pass

	@overload
	def updateFilePos(self) -> None:
		pass

	@overload
	def confirmDelete(self, f: FileChooser_fileObj) -> None:
		pass

	@overload
	def delete(self, f: FileChooser_fileObj) -> None:
		pass

	@overload
	def onScrollbar(self, page: float) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


