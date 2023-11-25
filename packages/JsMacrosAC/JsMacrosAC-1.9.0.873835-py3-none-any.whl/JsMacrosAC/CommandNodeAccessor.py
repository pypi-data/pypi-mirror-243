from typing import overload
from typing import TypeVar

com_mojang_brigadier_tree_CommandNode_S_ = TypeVar("com_mojang_brigadier_tree_CommandNode_S_")
CommandNode = com_mojang_brigadier_tree_CommandNode_S_


class CommandNodeAccessor:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def remove(self, parent: CommandNode, name: str) -> CommandNode:
		pass

	pass


