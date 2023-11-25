from typing import overload
from typing import TypeVar

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class AutoCompleteSuggestion:
	startIndex: int
	suggestion: str
	displayText: Text

	@overload
	def __init__(self, startIndex: int, suggestion: str) -> None:
		pass

	@overload
	def __init__(self, startIndex: int, suggestion: str, displayText: Text) -> None:
		pass

	pass


