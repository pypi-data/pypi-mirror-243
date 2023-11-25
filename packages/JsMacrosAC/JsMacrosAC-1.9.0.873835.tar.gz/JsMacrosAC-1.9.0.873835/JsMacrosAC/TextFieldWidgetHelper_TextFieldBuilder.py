from typing import overload
from typing import TypeVar
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .TextFieldWidgetHelper import TextFieldWidgetHelper

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class TextFieldWidgetHelper_TextFieldBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen, textRenderer: TextRenderer) -> None:
		pass

	@overload
	def getAction(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the callback for when the text is changed. 
		"""
		pass

	@overload
	def action(self, action: MethodWrapper) -> "TextFieldWidgetHelper_TextFieldBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the callback for when the text is changed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSuggestion(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current suggestion. 
		"""
		pass

	@overload
	def suggestion(self, suggestion: str) -> "TextFieldWidgetHelper_TextFieldBuilder":
		"""
		Since: 1.8.4 

		Args:
			suggestion: the suggestion to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> TextFieldWidgetHelper:
		pass

	pass


