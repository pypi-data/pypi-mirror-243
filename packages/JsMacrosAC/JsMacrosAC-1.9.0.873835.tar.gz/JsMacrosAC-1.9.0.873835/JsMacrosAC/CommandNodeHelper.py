from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

com_mojang_brigadier_tree_CommandNode = TypeVar("com_mojang_brigadier_tree_CommandNode")
CommandNode = com_mojang_brigadier_tree_CommandNode


class CommandNodeHelper(BaseHelper):
	fabric: CommandNode

	@overload
	def __init__(self, base: CommandNode, fabric: CommandNode) -> None:
		pass

	pass


