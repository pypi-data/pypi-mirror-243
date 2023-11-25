from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .PacketByteBufferHelper import PacketByteBufferHelper

net_minecraft_network_packet_Packet__ = TypeVar("net_minecraft_network_packet_Packet__")
Packet = net_minecraft_network_packet_Packet__


class EventRecvPacket(BaseEvent):
	"""
	Since: 1.8.4 
	"""
	packet: Packet
	type: str

	@overload
	def __init__(self, packet: Packet) -> None:
		pass

	@overload
	def getPacketBuffer(self) -> PacketByteBufferHelper:
		"""After modifying the buffer, use PacketByteBufferHelper#toPacket() to get the modified
packet and replace this packet with the modified one.\n
		Since: 1.8.4 

		Returns:
			a helper for accessing and modifying the packet's data. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


