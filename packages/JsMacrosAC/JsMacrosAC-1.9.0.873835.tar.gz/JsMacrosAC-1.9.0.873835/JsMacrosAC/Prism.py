from typing import overload
from typing import List
from typing import TypeVar
from typing import Set

io_noties_prism4j_Prism4j_Grammar = TypeVar("io_noties_prism4j_Prism4j_Grammar")
Prism4j_Grammar = io_noties_prism4j_Prism4j_Grammar

io_noties_prism4j_Prism4j_Node = TypeVar("io_noties_prism4j_Prism4j_Node")
Prism4j_Node = io_noties_prism4j_Prism4j_Node

io_noties_prism4j_GrammarLocator = TypeVar("io_noties_prism4j_GrammarLocator")
GrammarLocator = io_noties_prism4j_GrammarLocator

io_noties_prism4j_Prism4j = TypeVar("io_noties_prism4j_Prism4j")
Prism4j = io_noties_prism4j_Prism4j


class Prism(GrammarLocator):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getNodes(self, text: str, language: str) -> List[Prism4j_Node]:
		pass

	@overload
	def grammar(self, prism4j: Prism4j, language: str) -> Prism4j_Grammar:
		pass

	@overload
	def languages(self) -> Set[str]:
		pass

	pass


