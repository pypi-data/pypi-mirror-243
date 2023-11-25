from typing import overload
from .IEventListener import IEventListener
from .MethodWrapper import MethodWrapper


class FJsMacros_ScriptEventListener(IEventListener):

	@overload
	def getCreatorName(self) -> str:
		pass

	@overload
	def getWrapper(self) -> MethodWrapper:
		pass

	pass


