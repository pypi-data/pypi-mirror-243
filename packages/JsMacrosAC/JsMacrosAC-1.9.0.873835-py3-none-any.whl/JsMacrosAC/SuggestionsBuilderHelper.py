from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .BlockPosHelper import BlockPosHelper

com_mojang_brigadier_suggestion_SuggestionsBuilder = TypeVar("com_mojang_brigadier_suggestion_SuggestionsBuilder")
SuggestionsBuilder = com_mojang_brigadier_suggestion_SuggestionsBuilder


class SuggestionsBuilderHelper(BaseHelper):
	"""
	Since: 1.6.5 
	"""

	@overload
	def __init__(self, base: SuggestionsBuilder) -> None:
		pass

	@overload
	def getInput(self) -> str:
		pass

	@overload
	def getStart(self) -> int:
		pass

	@overload
	def getRemaining(self) -> str:
		pass

	@overload
	def getRemainingLowerCase(self) -> str:
		pass

	@overload
	def suggest(self, suggestion: str) -> "SuggestionsBuilderHelper":
		pass

	@overload
	def suggest(self, value: int) -> "SuggestionsBuilderHelper":
		pass

	@overload
	def suggestWithTooltip(self, suggestion: str, tooltip: TextHelper) -> "SuggestionsBuilderHelper":
		pass

	@overload
	def suggestWithTooltip(self, value: int, tooltip: TextHelper) -> "SuggestionsBuilderHelper":
		pass

	@overload
	def suggestMatching(self, suggestions: List[str]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			suggestions: the strings to match 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestMatching(self, suggestions: List[str]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			suggestions: the strings to match 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestIdentifier(self, identifiers: List[str]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			identifiers: the identifiers to match 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestIdentifier(self, identifiers: List[str]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			identifiers: the identifiers to match 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestBlockPositions(self, positions: List[BlockPosHelper]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			positions: the positions to suggest 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestBlockPositions(self, positions: List[BlockPosHelper]) -> "SuggestionsBuilderHelper":
		"""
		Since: 1.8.4 

		Args:
			positions: the positions to suggest 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestPositions(self, positions: List[str]) -> "SuggestionsBuilderHelper":
		"""Positions are strings of the form "x y z" where x, y, and z are numbers or the default
minecraft selectors "~" and "^" followed by a number.\n
		Since: 1.8.4 

		Args:
			positions: the positions to suggest 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def suggestPositions(self, positions: List[str]) -> "SuggestionsBuilderHelper":
		"""Positions are strings of the form "x y z" where x, y, and z are numbers or the default
minecraft selectors "~" and "^" followed by a number.\n
		Since: 1.8.4 

		Args:
			positions: the relative positions to suggest 

		Returns:
			self for chaining. 
		"""
		pass

	pass


