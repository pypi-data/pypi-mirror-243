from typing import overload
from typing import TypeVar

net_minecraft_network_packet_Packet__ = TypeVar("net_minecraft_network_packet_Packet__")
Packet = net_minecraft_network_packet_Packet__


class MixinClientConnection:
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def modifyReceivedPacket(self, packet: Packet) -> Packet:
		pass

	@overload
	def modifySendPacket(self, packet: Packet) -> Packet:
		pass

	pass


