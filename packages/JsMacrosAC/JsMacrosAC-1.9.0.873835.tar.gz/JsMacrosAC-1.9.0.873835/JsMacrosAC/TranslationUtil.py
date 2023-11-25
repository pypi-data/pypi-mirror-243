from typing import overload
from typing import TypeVar

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class TranslationUtil:
	"""
	Since: 1.6.4 
	"""

	@overload
	def getTranslatedEventName(self, eventName: str) -> Text:
		pass

	pass


