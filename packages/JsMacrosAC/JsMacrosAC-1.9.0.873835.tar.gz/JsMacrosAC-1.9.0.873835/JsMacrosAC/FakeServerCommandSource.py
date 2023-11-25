from typing import overload
from typing import List
from typing import TypeVar
from typing import Set

java_util_concurrent_CompletableFuture_com_mojang_brigadier_suggestion_Suggestions_ = TypeVar("java_util_concurrent_CompletableFuture_com_mojang_brigadier_suggestion_Suggestions_")
CompletableFuture = java_util_concurrent_CompletableFuture_com_mojang_brigadier_suggestion_Suggestions_

com_mojang_brigadier_context_CommandContext__ = TypeVar("com_mojang_brigadier_context_CommandContext__")
CommandContext = com_mojang_brigadier_context_CommandContext__

net_minecraft_client_network_ClientCommandSource = TypeVar("net_minecraft_client_network_ClientCommandSource")
ClientCommandSource = net_minecraft_client_network_ClientCommandSource

net_minecraft_command_CommandSource_RelativePosition = TypeVar("net_minecraft_command_CommandSource_RelativePosition")
CommandSource_RelativePosition = net_minecraft_command_CommandSource_RelativePosition

net_minecraft_registry_DynamicRegistryManager = TypeVar("net_minecraft_registry_DynamicRegistryManager")
DynamicRegistryManager = net_minecraft_registry_DynamicRegistryManager

java_util_stream_Stream_net_minecraft_util_Identifier_ = TypeVar("java_util_stream_Stream_net_minecraft_util_Identifier_")
Stream = java_util_stream_Stream_net_minecraft_util_Identifier_

java_util_function_Supplier_net_minecraft_text_Text_ = TypeVar("java_util_function_Supplier_net_minecraft_text_Text_")
Supplier = java_util_function_Supplier_net_minecraft_text_Text_

net_minecraft_client_network_ClientPlayerEntity = TypeVar("net_minecraft_client_network_ClientPlayerEntity")
ClientPlayerEntity = net_minecraft_client_network_ClientPlayerEntity

net_minecraft_registry_RegistryKey_net_minecraft_world_World_ = TypeVar("net_minecraft_registry_RegistryKey_net_minecraft_world_World_")
RegistryKey = net_minecraft_registry_RegistryKey_net_minecraft_world_World_

net_minecraft_server_command_ServerCommandSource = TypeVar("net_minecraft_server_command_ServerCommandSource")
ServerCommandSource = net_minecraft_server_command_ServerCommandSource


class FakeServerCommandSource(ServerCommandSource):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, source: ClientCommandSource, player: ClientPlayerEntity) -> None:
		pass

	@overload
	def getEntitySuggestions(self) -> List[str]:
		pass

	@overload
	def getChatSuggestions(self) -> List[str]:
		pass

	@overload
	def getPlayerNames(self) -> List[str]:
		pass

	@overload
	def getTeamNames(self) -> List[str]:
		pass

	@overload
	def getSoundIds(self) -> Stream:
		pass

	@overload
	def getRecipeIds(self) -> Stream:
		pass

	@overload
	def getCompletions(self, context: CommandContext) -> CompletableFuture:
		pass

	@overload
	def getBlockPositionSuggestions(self) -> List[CommandSource_RelativePosition]:
		pass

	@overload
	def getPositionSuggestions(self) -> List[CommandSource_RelativePosition]:
		pass

	@overload
	def getWorldKeys(self) -> Set[RegistryKey]:
		pass

	@overload
	def getRegistryManager(self) -> DynamicRegistryManager:
		pass

	@overload
	def sendFeedback(self, feedbackSupplier: Supplier, broadcastToOps: bool) -> None:
		pass

	pass


