from typing import overload
from typing import List
from .CommandBuilder import CommandBuilder
from .CommandNodeHelper import CommandNodeHelper
from .MethodWrapper import MethodWrapper


class CommandManager:
	"""
	Since: 1.7.0 
	"""
	instance: "CommandManager"

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getValidCommands(self) -> List[str]:
		"""
		Since: 1.7.0 

		Returns:
			list of commands 
		"""
		pass

	@overload
	def createCommandBuilder(self, name: str) -> CommandBuilder:
		"""
		Since: 1.7.0 

		Args:
			name: 
		"""
		pass

	@overload
	def unregisterCommand(self, command: str) -> CommandNodeHelper:
		"""
		Since: 1.7.0 

		Args:
			command: 
		"""
		pass

	@overload
	def reRegisterCommand(self, node: CommandNodeHelper) -> None:
		"""warning: this method is hacky\n
		Since: 1.7.0 

		Args:
			node: 
		"""
		pass

	@overload
	def getArgumentAutocompleteOptions(self, commandPart: str, callback: MethodWrapper) -> None:
		"""
		Since: 1.8.2 

		Args:
			commandPart: 
		"""
		pass

	pass


