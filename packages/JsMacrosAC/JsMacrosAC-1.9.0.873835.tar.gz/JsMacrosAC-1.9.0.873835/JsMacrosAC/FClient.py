from typing import overload
from typing import List
from typing import TypeVar
from typing import Any
from .PerExecLibrary import PerExecLibrary
from .TickSync import TickSync
from .BaseScriptContext import BaseScriptContext
from .RegistryHelper import RegistryHelper
from .PacketByteBufferHelper import PacketByteBufferHelper
from .MethodWrapper import MethodWrapper
from .OptionsHelper import OptionsHelper
from .ServerInfoHelper import ServerInfoHelper
from .ModContainerHelper import ModContainerHelper
from .BlockHelper import BlockHelper
from .ItemHelper import ItemHelper

net_minecraft_network_packet_Packet_net_minecraft_network_listener_ClientPlayPacketListener_ = TypeVar("net_minecraft_network_packet_Packet_net_minecraft_network_listener_ClientPlayPacketListener_")
Packet = net_minecraft_network_packet_Packet_net_minecraft_network_listener_ClientPlayPacketListener_

net_minecraft_client_MinecraftClient = TypeVar("net_minecraft_client_MinecraftClient")
MinecraftClient = net_minecraft_client_MinecraftClient


class FClient(PerExecLibrary):
	"""Functions that interact with minecraft that don't fit into their own module. 
An instance of this class is passed to scripts as the 'Client' variable.\n
	Since: 1.2.9 
	"""
	tickSynchronizer: TickSync

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def getMinecraft(self) -> MinecraftClient:
		"""
		Since: 1.0.0 (was in the 'jsmacros' library until 1.2.9) 

		Returns:
			the raw minecraft client class, it may be useful to use Minecraft Mappings Viewer for this. 
		"""
		pass

	@overload
	def getRegistryManager(self) -> RegistryHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for interacting with minecraft's registry. 
		"""
		pass

	@overload
	def createPacketByteBuffer(self) -> PacketByteBufferHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper to modify and send minecraft packets. 
		"""
		pass

	@overload
	def runOnMainThread(self, runnable: MethodWrapper) -> None:
		"""Run your task on the main minecraft thread\n
		Since: 1.4.0 

		Args:
			runnable: task to run 
		"""
		pass

	@overload
	def runOnMainThread(self, runnable: MethodWrapper, watchdogMaxTime: float) -> None:
		"""
		Since: 1.6.5 

		Args:
			runnable: 
			watchdogMaxTime: max time for the watchdog to wait before killing the script 
		"""
		pass

	@overload
	def getGameOptions(self) -> OptionsHelper:
		"""
		Since: 1.1.7 (was in the 'jsmacros' library until 1.2.9) 

		Returns:
			a helper which gives access to all game options and some other useful features. 
		"""
		pass

	@overload
	def mcVersion(self) -> str:
		"""
		Since: 1.1.2 (was in the 'jsmacros' library until 1.2.9) 

		Returns:
			the current minecraft version as a String . 
		"""
		pass

	@overload
	def getFPS(self) -> str:
		"""
		Since: 1.2.0 (was in the 'jsmacros' library until 1.2.9) 

		Returns:
			the fps debug string from minecraft. 
		"""
		pass

	@overload
	def loadWorld(self, folderName: str) -> None:
		"""Join singleplayer world\n
		Since: 1.6.6 

		Args:
			folderName: 
		"""
		pass

	@overload
	def connect(self, ip: str) -> None:
		"""
		Since: 1.2.3 (was in the 'jsmacros' library until 1.2.9) 

		Args:
			ip: 
		"""
		pass

	@overload
	def connect(self, ip: str, port: int) -> None:
		"""Connect to a server\n
		Since: 1.2.3 (was in the 'jsmacros' library until 1.2.9) 

		Args:
			port: 
			ip: 
		"""
		pass

	@overload
	def disconnect(self) -> None:
		"""
		Since: 1.2.3 (was in the 'jsmacros' library until 1.2.9) 
		"""
		pass

	@overload
	def disconnect(self, callback: MethodWrapper) -> None:
		"""Disconnect from a server with callback.\n
		Since: 1.2.3 (was in the 'jsmacros' library until 1.2.9) 
'callback' defaults to 'null' 

		Args:
			callback: calls your method as a Consumer Boolean 
		"""
		pass

	@overload
	def shutdown(self) -> None:
		"""Closes the client (stops the game).
Waits until the game has stopped, meaning no further code is executed (for obvious reasons).
Warning: this does not wait on joined threads, so your script may stop at an undefined point.\n
		Since: 1.6.0 
		"""
		pass

	@overload
	def waitTick(self) -> None:
		"""
		Since: 1.2.4 
		"""
		pass

	@overload
	def waitTick(self, i: int) -> None:
		"""waits the specified number of client ticks.
don't use this on an event that the main thread waits on (joins)... that'll cause circular waiting.\n
		Since: 1.2.6 

		Args:
			i: 
		"""
		pass

	@overload
	def ping(self, ip: str) -> ServerInfoHelper:
		"""
		Since: 1.6.5 

		Args:
			ip: 
		"""
		pass

	@overload
	def pingAsync(self, ip: str, callback: MethodWrapper) -> None:
		"""
		Since: 1.6.5 

		Args:
			ip: 
			callback: 
		"""
		pass

	@overload
	def cancelAllPings(self) -> None:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getLoadedMods(self) -> List[Any]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all loaded mods. 
		"""
		pass

	@overload
	def isModLoaded(self, modId: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			modId: the mod modId 

		Returns:
			'true' if the mod with the given modId is loaded, 'false' otherwise. 
		"""
		pass

	@overload
	def getMod(self, modId: str) -> ModContainerHelper:
		"""
		Since: 1.8.4 

		Args:
			modId: the mod modId 

		Returns:
			the mod container for the given modId or 'null' if the mod is not loaded. 
		"""
		pass

	@overload
	def grabMouse(self) -> None:
		"""Makes minecraft believe that the mouse is currently inside the window.
This will automatically set pause on lost focus to false.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isDevEnv(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the mod is loaded inside a development environment, 'false' otherwise. 
		"""
		pass

	@overload
	def getModLoader(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the mod loader. 
		"""
		pass

	@overload
	def getRegisteredBlocks(self) -> List[BlockHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all loaded blocks as BlockHelper objects. 
		"""
		pass

	@overload
	def getRegisteredItems(self) -> List[ItemHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all loaded items as ItemHelper objects. 
		"""
		pass

	@overload
	def exitGamePeacefully(self) -> None:
		"""Tries to peacefully close the game.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def exitGameForcefully(self) -> None:
		"""Will close the game forcefully.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def sendPacket(self, packet: Packet) -> None:
		"""
		Since: 1.8.4 

		Args:
			packet: the packet to send 
		"""
		pass

	@overload
	def receivePacket(self, packet: Packet) -> None:
		"""
		Since: 1.8.4 

		Args:
			packet: the packet to receive 
		"""
		pass

	pass


