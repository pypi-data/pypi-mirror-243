from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .MethodWrapper import MethodWrapper
from .BlockPosHelper import BlockPosHelper
from .ChunkHelper import ChunkHelper
from .Pair import Pair
from .TextBuilder import TextBuilder
from .TextHelper import TextHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper
from .NBTElementHelper import NBTElementHelper
from .ItemStackHelper import ItemStackHelper
from .Pos3D import Pos3D

net_minecraft_network_packet_Packet__ = TypeVar("net_minecraft_network_packet_Packet__")
Packet = net_minecraft_network_packet_Packet__

net_minecraft_util_collection_IndexedIterable_T_ = TypeVar("net_minecraft_util_collection_IndexedIterable_T_")
IndexedIterable = net_minecraft_util_collection_IndexedIterable_T_

java_util_Optional_T_ = TypeVar("java_util_Optional_T_")
Optional = java_util_Optional_T_

java_util_BitSet = TypeVar("java_util_BitSet")
BitSet = java_util_BitSet

K = TypeVar("K")
K = K

L = TypeVar("L")
L = L

java_util_Date = TypeVar("java_util_Date")
Date = java_util_Date

java_util_function_Function_net_minecraft_network_PacketByteBuf, extends net_minecraft_network_packet_Packet___ = TypeVar("java_util_function_Function_net_minecraft_network_PacketByteBuf, extends net_minecraft_network_packet_Packet___")
Function = java_util_function_Function_net_minecraft_network_PacketByteBuf, extends net_minecraft_network_packet_Packet___

R = TypeVar("R")
T = TypeVar("T")
com_mojang_authlib_GameProfile = TypeVar("com_mojang_authlib_GameProfile")
GameProfile = com_mojang_authlib_GameProfile

V = TypeVar("V")
V = V

net_minecraft_network_PacketByteBuf = TypeVar("net_minecraft_network_PacketByteBuf")
PacketByteBuf = net_minecraft_network_PacketByteBuf

java_util_UUID = TypeVar("java_util_UUID")
UUID = java_util_UUID

net_minecraft_util_hit_BlockHitResult = TypeVar("net_minecraft_util_hit_BlockHitResult")
BlockHitResult = net_minecraft_util_hit_BlockHitResult

net_minecraft_registry_RegistryKey_T_ = TypeVar("net_minecraft_registry_RegistryKey_T_")
RegistryKey = net_minecraft_registry_RegistryKey_T_


class PacketByteBufferHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""
	BUFFER_TO_PACKET: Mapping[Class, Function]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def __init__(self, base: PacketByteBuf) -> None:
		pass

	@overload
	def __init__(self, packet: Packet) -> None:
		pass

	@overload
	def toPacket(self) -> Packet:
		"""
		Since: 1.8.4 

		Returns:
			the packet for this buffer or 'null' if no packet was used to create this
helper. 
		"""
		pass

	@overload
	def toPacket(self, packetName: str) -> Packet:
		"""
		Since: 1.8.4 

		Args:
			packetName: the name of the packet's class that should be returned 

		Returns:
			the packet for this buffer. 
		"""
		pass

	@overload
	def toPacket(self, clazz: Class) -> Packet:
		"""
		Since: 1.8.4 

		Args:
			clazz: the class of the packet to return 

		Returns:
			the packet for this buffer. 
		"""
		pass

	@overload
	def toPacket(self, clientbound: bool, packetId: int) -> Packet:
		"""
		Since: 1.8.4 

		Args:
			packetId: the id of the packet 
			clientbound: whether the packet is clientbound or serverbound 

		Returns:
			the packet for this buffer. 
		"""
		pass

	@overload
	def getPacketId(self, packetClass: Class) -> int:
		"""
		Since: 1.8.4 

		Args:
			packetClass: the class of the packet to get the id for 

		Returns:
			the id of the packet. 
		"""
		pass

	@overload
	def getNetworkStateId(self, packetClass: Class) -> int:
		"""
		Since: 1.8.4 

		Args:
			packetClass: the class of the packet to get the id for 

		Returns:
			the id of the network state the packet belongs to. 
		"""
		pass

	@overload
	def isClientbound(self, packetClass: Class) -> bool:
		"""
		Since: 1.8.4 

		Args:
			packetClass: the class to get the side for 

		Returns:
			'true' if the packet is clientbound, 'false' if it is serverbound. 
		"""
		pass

	@overload
	def isServerbound(self, packetClass: Class) -> bool:
		"""
		Since: 1.8.4 

		Args:
			packetClass: the class to get the id for 

		Returns:
			'true' if the packet is serverbound, 'false' if it is clientbound. 
		"""
		pass

	@overload
	def sendPacket(self) -> "PacketByteBufferHelper":
		"""Send a packet of the given type, created from this buffer, to the server.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def sendPacket(self, packetName: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			packetName: the name of the packet's class that should be sent 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def sendPacket(self, clazz: Class) -> "PacketByteBufferHelper":
		"""Send a packet of the given type, created from this buffer, to the server.\n
		Since: 1.8.4 

		Args:
			clazz: the class of the packet to send 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def sendCustomPacket(self, channel: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			channel: the channel to send the packet on 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def receivePacket(self) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def receivePacket(self, packetName: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			packetName: the name of the packet's class that should be received 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def receivePacket(self, clazz: Class) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			clazz: the class of the packet to receive 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def receiveCustomPacket(self, channel: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			channel: the channel to receive the packet on 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPacketNames(self) -> List[str]:
		"""These names are subject to change and are only for an easier access. They will probably not
change in the future, but it is not guaranteed.\n
		Since: 1.8.4 

		Returns:
			a list of all packet names. 
		"""
		pass

	@overload
	def reset(self) -> "PacketByteBufferHelper":
		"""Resets the buffer to the state it was in when this helper was created.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeRegistryValue(self, registry: IndexedIterable, value: T) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			registry: the registry the value is from 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readRegistryValue(self, registry: IndexedIterable) -> T:
		"""
		Since: 1.8.4 

		Args:
			registry: the registry the read value is from 

		Returns:
			the registry value. 
		"""
		pass

	@overload
	def writeRegistryKey(self, key: RegistryKey) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			key: the registry key to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readRegistryKey(self, registry: RegistryKey) -> RegistryKey:
		"""
		Since: 1.8.4 

		Args:
			registry: the registry the read key is from 

		Returns:
			the registry key. 
		"""
		pass

	@overload
	def writeCollection(self, collection: List[T], writer: MethodWrapper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			collection: the collection to store 
			writer: the function that writes the collection's elements to the buffer 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readList(self, reader: MethodWrapper) -> List[T]:
		"""
		Since: 1.8.4 

		Args:
			reader: the function that reads the collection's elements from the buffer 

		Returns:
			the read list. 
		"""
		pass

	@overload
	def writeIntList(self, list: List[int]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			list: the integer list to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readIntList(self) -> IntList:
		"""
		Since: 1.8.4 

		Returns:
			the read integer list. 
		"""
		pass

	@overload
	def writeMap(self, map: Mapping[K, V], keyWriter: MethodWrapper, valueWriter: MethodWrapper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			keyWriter: the function to write the map's keys to the buffer 
			map: the map to store 
			valueWriter: the function to write the map's values to the buffer 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readMap(self, keyReader: MethodWrapper, valueReader: MethodWrapper) -> Mapping[K, V]:
		"""
		Since: 1.8.4 

		Args:
			valueReader: the function to read the map's values from the buffer 
			keyReader: the function to read the map's keys from the buffer 

		Returns:
			the read map. 
		"""
		pass

	@overload
	def forEachInCollection(self, reader: MethodWrapper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			reader: the function to read the collection's elements from the buffer 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeOptional(self, value: T, writer: MethodWrapper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			writer: the function to write the optional value if present to the buffer 
			value: the optional value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readOptional(self, reader: MethodWrapper) -> Optional:
		"""
		Since: 1.8.4 

		Args:
			reader: the function to read the optional value from the buffer if present 

		Returns:
			the optional value. 
		"""
		pass

	@overload
	def writeNullable(self, value: object, writer: MethodWrapper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			writer: the function to write the optional value if it's not null to the buffer 
			value: the optional value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readNullable(self, reader: MethodWrapper) -> T:
		"""
		Since: 1.8.4 

		Args:
			reader: the function to read the value from the buffer if it's not null 

		Returns:
			the read value or 'null' if it was null. 
		"""
		pass

	@overload
	def writeEither(self, left: L, right: R, leftWriter: MethodWrapper, rightWriter: MethodWrapper) -> "PacketByteBufferHelper":
		"""This method chooses the left value if it's not null, otherwise it chooses the right value.\n
		Since: 1.8.4 

		Args:
			left: the left value to store 
			rightWriter: the function to write the right value to the buffer 
			leftWriter: the function to write the left value to the buffer 
			right: the right value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readEither(self, leftReader: MethodWrapper, rightReader: MethodWrapper) -> object:
		"""
		Since: 1.8.4 

		Args:
			rightReader: the function to read the right value from the buffer 
			leftReader: the function to read the left value from the buffer 

		Returns:
			the read object. 
		"""
		pass

	@overload
	def writeByteArray(self, bytes: List[float]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			bytes: the bytes to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readByteArray(self) -> List[float]:
		"""
		Since: 1.8.4 

		Returns:
			the read byte array. 
		"""
		pass

	@overload
	def readByteArray(self, maxSize: int) -> List[float]:
		"""Will throw an exception if the byte array is bigger than the given maximum size.\n
		Since: 1.8.4 

		Args:
			maxSize: the maximum size of the byte array to read 

		Returns:
			the read byte array. 
		"""
		pass

	@overload
	def writeIntArray(self, ints: List[int]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			ints: the int array to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readIntArray(self) -> List[int]:
		"""
		Since: 1.8.4 

		Returns:
			the read int array. 
		"""
		pass

	@overload
	def readIntArray(self, maxSize: int) -> "PacketByteBufferHelper":
		"""Will throw an exception if the int array is bigger than the given maximum size.\n
		Since: 1.8.4 

		Args:
			maxSize: the maximum size of the int array to read 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeLongArray(self, longs: List[float]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			longs: the long array to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readLongArray(self) -> List[float]:
		"""
		Since: 1.8.4 

		Returns:
			the read long array. 
		"""
		pass

	@overload
	def readLongArray(self, maxSize: int) -> List[float]:
		"""Will throw an exception if the long array is bigger than the given maximum size.\n
		Since: 1.8.4 

		Args:
			maxSize: the maximum size of the long array to read 

		Returns:
			the read long array. 
		"""
		pass

	@overload
	def writeBlockPos(self, pos: BlockPosHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			pos: the block position to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeBlockPos(self, x: int, y: int, z: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the block position to store 
			y: the y coordinate of the block position to store 
			z: the z coordinate of the block position to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readBlockPos(self) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Returns:
			the read block position. 
		"""
		pass

	@overload
	def writeChunkPos(self, x: int, z: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the chunk to store 
			z: the z coordinate of the chunk to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeChunkPos(self, chunk: ChunkHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			chunk: the chunk to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readChunkPos(self) -> List[int]:
		"""
		Since: 1.8.4 

		Returns:
			the position of the read chunk, x at index 0, z at index 1. 
		"""
		pass

	@overload
	def readChunkHelper(self) -> ChunkHelper:
		"""
		Since: 1.8.4 

		Returns:
			a ChunkHelper for the read chunk position. 
		"""
		pass

	@overload
	def writeChunkSectionPos(self, chunkX: int, y: int, chunkZ: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			y: the y coordinate to store 
			chunkX: the x coordinate of the chunk to store 
			chunkZ: the z coordinate of the chunk to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeChunkSectionPos(self, chunk: ChunkHelper, y: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			chunk: the chunk whose position should be stored 
			y: the y to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readChunkSectionPos(self) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Returns:
			the read chunk section pos, as a BlockPosHelper . 
		"""
		pass

	@overload
	def writeGlobalPos(self, dimension: str, pos: BlockPosHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			pos: the position to store 
			dimension: the dimension, vanilla default are 'overworld' , 'the_nether' , 'the_end' 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeGlobalPos(self, dimension: str, x: int, y: int, z: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the position to store 
			y: the y coordinate of the position to store 
			z: the z coordinate of the position to store 
			dimension: the dimension, vanilla default are 'overworld' , 'the_nether' , 'the_end' 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readGlobalPos(self) -> Pair:
		"""
		Since: 1.8.4 

		Returns:
			the read global pos, the first element is the dimension, the second is the position. 
		"""
		pass

	@overload
	def writeText(self, text: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			text: the string to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeText(self, builder: TextBuilder) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			builder: the text builder whose text should be stored 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeText(self, text: TextHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			text: the text to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readText(self) -> TextHelper:
		"""
		Since: 1.8.4 

		Returns:
			the read text. 
		"""
		pass

	@overload
	def writeEnumConstant(self, constant: ) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			constant: the enum constant to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readEnumConstant(self, enumClass: Class) -> T:
		"""
		Since: 1.8.4 

		Args:
			enumClass: the class of the enum to read from 

		Returns:
			the read enum constant. 
		"""
		pass

	@overload
	def writeVarInt(self, i: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			i: the int to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readVarInt(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the read int. 
		"""
		pass

	@overload
	def writeVarLong(self, l: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			l: the long to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readVarLong(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read long. 
		"""
		pass

	@overload
	def writeUuid(self, uuid: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			uuid: the UUID to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readUuid(self) -> UUID:
		"""
		Since: 1.8.4 

		Returns:
			the read UUID. 
		"""
		pass

	@overload
	def writeNbt(self, nbt: NBTElementHelper_NBTCompoundHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			nbt: the nbt 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readNbt(self) -> NBTElementHelper:
		"""
		Since: 1.8.4 

		Returns:
			the read nbt data. 
		"""
		pass

	@overload
	def writeItemStack(self, stack: ItemStackHelper) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			stack: the item stack to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readItemStack(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the read item stack. 
		"""
		pass

	@overload
	def writeString(self, string: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			string: the string to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeString(self, string: str, maxLength: int) -> "PacketByteBufferHelper":
		"""Throws an exception if the string is longer than the given length.\n
		Since: 1.8.4 

		Args:
			string: the string to store 
			maxLength: the maximum length of the string 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readString(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the read string. 
		"""
		pass

	@overload
	def readString(self, maxLength: int) -> str:
		"""Throws an exception if the read string is longer than the given length.\n
		Since: 1.8.4 

		Args:
			maxLength: the maximum length of the string to read 

		Returns:
			the read string. 
		"""
		pass

	@overload
	def writeIdentifier(self, id: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			id: the identifier to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readIdentifier(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the read identifier. 
		"""
		pass

	@overload
	def writeDate(self, date: Date) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			date: the date to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readDate(self) -> Date:
		"""
		Since: 1.8.4 

		Returns:
			the read date. 
		"""
		pass

	@overload
	def writeInstant(self, instant: Instant) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			instant: the instant to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readInstant(self) -> Instant:
		"""
		Since: 1.8.4 

		Returns:
			the read instant. 
		"""
		pass

	@overload
	def writePublicKey(self, key: PublicKey) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			key: the public key to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readPublicKey(self) -> PublicKey:
		"""
		Since: 1.8.4 

		Returns:
			the read public key. 
		"""
		pass

	@overload
	def writeBlockHitResult(self, hitResult: BlockHitResult) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			hitResult: the hit result to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeBlockHitResult(self, pos: Pos3D, direction: str, blockPos: BlockPosHelper, missed: bool, insideBlock: bool) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			insideBlock: whether the BlockHitResult is inside a block 
			blockPos: the block pos of the BlockHitResult 
			pos: the position of the BlockHitResult 
			missed: whether the BlockHitResult missed 
			direction: the direction of the BlockHitResult 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readBlockHitResult(self) -> BlockHitResult:
		"""
		Since: 1.8.4 

		Returns:
			the read block hit result. 
		"""
		pass

	@overload
	def readBlockHitResultMap(self) -> Mapping[str, object]:
		"""
		Since: 1.8.4 

		Returns:
			a map of the block hit result's data and their values. 
		"""
		pass

	@overload
	def writeBitSet(self, bitSet: BitSet) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			bitSet: the bit set to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readBitSet(self) -> BitSet:
		"""
		Since: 1.8.4 

		Returns:
			the read bit set. 
		"""
		pass

	@overload
	def writeGameProfile(self, profile: GameProfile) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			profile: the profile to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readGameProfile(self) -> GameProfile:
		"""
		Since: 1.8.4 

		Returns:
			the read game profile. 
		"""
		pass

	@overload
	def readGameProfileName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the read profile's name. 
		"""
		pass

	@overload
	def readGameProfileUuid(self) -> UUID:
		"""
		Since: 1.8.4 

		Returns:
			the read profile's UUID. 
		"""
		pass

	@overload
	def readerIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the readers current position. 
		"""
		pass

	@overload
	def setReaderIndex(self, index: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the readers new index 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writerIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the writers current position. 
		"""
		pass

	@overload
	def setWriterIndex(self, index: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the writers new index 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setIndices(self, readerIndex: int, writerIndex: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			readerIndex: the readers new index 
			writerIndex: the writers new index 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def resetIndices(self) -> "PacketByteBufferHelper":
		"""Resets the readers and writers index to their respective last marked indices.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def markReaderIndex(self) -> "PacketByteBufferHelper":
		"""Marks the readers current index for later use.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def resetReaderIndex(self) -> "PacketByteBufferHelper":
		"""Resets the readers index to the last marked index.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def markWriterIndex(self) -> "PacketByteBufferHelper":
		"""Marks the writers current index for later use.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def resetWriterIndex(self) -> "PacketByteBufferHelper":
		"""Resets the writers index to the last marked index.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def clear(self) -> "PacketByteBufferHelper":
		"""Resets the writers and readers index to 0. This technically doesn't clear the buffer, but
rather makes it so that new operations will overwrite the old data.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeBoolean(self, value: bool) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setBoolean(self, index: int, value: bool) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readBoolean(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			the read boolean value. 
		"""
		pass

	@overload
	def getBoolean(self, index: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the boolean value at the given index. 
		"""
		pass

	@overload
	def writeChar(self, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setChar(self, index: int, value: str) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readChar(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the read char value. 
		"""
		pass

	@overload
	def getChar(self, index: int) -> str:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the char at the given index. 
		"""
		pass

	@overload
	def writeByte(self, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setByte(self, index: int, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readByte(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read byte value. 
		"""
		pass

	@overload
	def readUnsignedByte(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read unsigned byte value, represented as a short. 
		"""
		pass

	@overload
	def getByte(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the byte at the given index. 
		"""
		pass

	@overload
	def getUnsignedByte(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the unsigned byte at the given index, represented as a short. 
		"""
		pass

	@overload
	def writeShort(self, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setShort(self, index: int, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readShort(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read short value. 
		"""
		pass

	@overload
	def readUnsignedShort(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the read unsigned short value, represented as an int. 
		"""
		pass

	@overload
	def getShort(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the short at the given index. 
		"""
		pass

	@overload
	def getUnsignedShort(self, index: int) -> int:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the unsigned short at the given index, represented as an int. 
		"""
		pass

	@overload
	def writeMedium(self, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setMedium(self, index: int, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readMedium(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the read medium value. 
		"""
		pass

	@overload
	def readUnsignedMedium(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the read unsigned medium value. 
		"""
		pass

	@overload
	def getMedium(self, index: int) -> int:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the medium at the given index. 
		"""
		pass

	@overload
	def getUnsignedMedium(self, index: int) -> int:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the unsigned medium at the given index. 
		"""
		pass

	@overload
	def writeInt(self, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setInt(self, index: int, value: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readInt(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the read int value. 
		"""
		pass

	@overload
	def readUnsignedInt(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read unsigned int value, represented as a long. 
		"""
		pass

	@overload
	def getInt(self, index: int) -> int:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the int at the given index. 
		"""
		pass

	@overload
	def getUnsignedInt(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the unsigned int at the given index, represented as a long. 
		"""
		pass

	@overload
	def writeLong(self, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setLong(self, index: int, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readLong(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read long value. 
		"""
		pass

	@overload
	def getLong(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the long at the given index. 
		"""
		pass

	@overload
	def writeFloat(self, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setFloat(self, index: int, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readFloat(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read float value. 
		"""
		pass

	@overload
	def getFloat(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the float at the given index. 
		"""
		pass

	@overload
	def writeDouble(self, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setDouble(self, index: int, value: float) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			index: the index to write to 
			value: the value to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readDouble(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the read double value. 
		"""
		pass

	@overload
	def getDouble(self, index: int) -> float:
		"""
		Since: 1.8.4 

		Args:
			index: the index to read from 

		Returns:
			the double at the given index. 
		"""
		pass

	@overload
	def writeZero(self, length: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			length: the amount of zeros to write 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setZero(self, index: int, length: int) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			length: the amount of zeros to write 
			index: the index to write to 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def writeBytes(self, bytes: List[float]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			bytes: the bytes to store 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setBytes(self, index: int, bytes: List[float]) -> "PacketByteBufferHelper":
		"""
		Since: 1.8.4 

		Args:
			bytes: the bytes to store 
			index: the index to write to 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def readBytes(self, length: int) -> List[float]:
		"""Starts reading from this buffer's readerIndex.\n
		Since: 1.8.4 

		Args:
			length: the length of the array to read 

		Returns:
			the read byte array. 
		"""
		pass

	@overload
	def getBytes(self, index: int, length: int) -> List[float]:
		"""
		Since: 1.8.4 

		Args:
			length: the length of the array to read 
			index: the index to start reading from 

		Returns:
			the read byte array . 
		"""
		pass

	@overload
	def skipBytes(self, length: int) -> "PacketByteBufferHelper":
		"""Moves the readerIndex of this buffer by the specified amount.\n
		Since: 1.8.4 

		Args:
			length: the amount of bytes to skip 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def getPacketName(self, packet: Packet) -> str:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def main(self, args: List[str]) -> None:
		pass

	pass


