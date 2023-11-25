from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent

com_mojang_brigadier_context_CommandContext__ = TypeVar("com_mojang_brigadier_context_CommandContext__")
CommandContext = com_mojang_brigadier_context_CommandContext__

com_mojang_brigadier_context_StringRange = TypeVar("com_mojang_brigadier_context_StringRange")
StringRange = com_mojang_brigadier_context_StringRange


class CommandContextHelper(BaseEvent):
	"""
	Since: 1.4.2 
	"""

	@overload
	def __init__(self, base: CommandContext) -> None:
		pass

	@overload
	def getRaw(self) -> CommandContext:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def equals(self, obj: object) -> bool:
		pass

	@overload
	def getArg(self, name: str) -> object:
		"""
		Since: 1.4.2 

		Args:
			name: 
		"""
		pass

	@overload
	def getChild(self) -> "CommandContextHelper":
		pass

	@overload
	def getRange(self) -> StringRange:
		pass

	@overload
	def getInput(self) -> str:
		pass

	pass


