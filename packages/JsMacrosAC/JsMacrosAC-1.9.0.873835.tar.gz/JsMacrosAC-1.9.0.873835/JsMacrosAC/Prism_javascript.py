from typing import overload
from typing import TypeVar

io_noties_prism4j_Prism4j_Grammar = TypeVar("io_noties_prism4j_Prism4j_Grammar")
Prism4j_Grammar = io_noties_prism4j_Prism4j_Grammar

io_noties_prism4j_Prism4j = TypeVar("io_noties_prism4j_Prism4j")
Prism4j = io_noties_prism4j_Prism4j


class Prism_javascript:
	"""This class is from Prism4j under the Apache-2.0 license I updated template-strings to match with the JS version again, which made them work better. other updates.
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def create(self, prism4j: Prism4j) -> Prism4j_Grammar:
		pass

	pass


