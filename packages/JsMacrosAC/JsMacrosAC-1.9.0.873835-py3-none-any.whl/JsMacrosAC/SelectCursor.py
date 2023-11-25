from typing import overload
from typing import TypeVar

java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_gui_editor_SelectCursor_ = TypeVar("java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_gui_editor_SelectCursor_")
Consumer = java_util_function_Consumer_xyz_wagyourtail_jsmacros_client_gui_editor_SelectCursor_

net_minecraft_text_Style = TypeVar("net_minecraft_text_Style")
Style = net_minecraft_text_Style


class SelectCursor:
	onChange: Consumer
	defaultStyle: Style
	startLine: int
	endLine: int
	startIndex: int
	endIndex: int
	startLineIndex: int
	endLineIndex: int
	dragStartIndex: int
	arrowLineIndex: int
	arrowEnd: bool
	startCol: int
	endCol: int

	@overload
	def __init__(self, defaultStyle: Style) -> None:
		pass

	@overload
	def updateStartIndex(self, startIndex: int, current: str) -> None:
		pass

	@overload
	def updateEndIndex(self, endIndex: int, current: str) -> None:
		pass

	pass


