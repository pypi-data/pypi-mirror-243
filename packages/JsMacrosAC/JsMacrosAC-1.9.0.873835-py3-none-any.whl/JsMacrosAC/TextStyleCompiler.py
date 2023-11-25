from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

net_minecraft_text_MutableText = TypeVar("net_minecraft_text_MutableText")
MutableText = net_minecraft_text_MutableText

io_noties_prism4j_AbsVisitor = TypeVar("io_noties_prism4j_AbsVisitor")
AbsVisitor = io_noties_prism4j_AbsVisitor

net_minecraft_text_Style = TypeVar("net_minecraft_text_Style")
Style = net_minecraft_text_Style


class TextStyleCompiler(AbsVisitor):

	@overload
	def __init__(self, defaultStyle: Style, themeData: Mapping[str, List[float]]) -> None:
		pass

	@overload
	def getResult(self) -> List[MutableText]:
		pass

	pass


