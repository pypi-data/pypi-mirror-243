from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Pos3D import Pos3D

java_util_function_Function_xyz_wagyourtail_jsmacros_client_api_helpers_world_BlockStateHelper,java_lang_Boolean_ = TypeVar("java_util_function_Function_xyz_wagyourtail_jsmacros_client_api_helpers_world_BlockStateHelper,java_lang_Boolean_")
Function = java_util_function_Function_xyz_wagyourtail_jsmacros_client_api_helpers_world_BlockStateHelper,java_lang_Boolean_

net_minecraft_util_math_ChunkPos = TypeVar("net_minecraft_util_math_ChunkPos")
ChunkPos = net_minecraft_util_math_ChunkPos

net_minecraft_world_World = TypeVar("net_minecraft_world_World")
World = net_minecraft_world_World


class WorldScanner:
	"""A class to scan the world for certain blocks. The results of the filters are cached,
so it's a good idea to reuse an instance of this if possible.
The scanner can either return a list of all block positions or
a list of blocks and their respective count for every block / state matching the filters criteria.\n
	Since: 1.6.5 
	"""

	@overload
	def __init__(self, world: World, blockFilter: Function, stateFilter: Function) -> None:
		"""Creates a new World scanner with for the given world. It accepts two boolean functions,
one for BlockHelper and the other for BlockStateHelper .

		Args:
			world: the world to scan 
			blockFilter: a filter method for the blocks 
			stateFilter: a filter method for the block states 
		"""
		pass

	@overload
	def getChunkRange(self, centerX: int, centerZ: int, chunkrange: int) -> List[ChunkPos]:
		"""Gets a list of all chunks in the given range around the center chunk.

		Args:
			centerZ: the z coordinate of the center chunk to scan around 
			centerX: the x coordinate of the center chunk to scan around 
			chunkrange: the range to scan around the center chunk 

		Returns:
			a list of all matching block positions. 
		"""
		pass

	@overload
	def scanAroundPlayer(self, chunkRange: int) -> List[Pos3D]:
		"""Scans all chunks in the given range around the player and returns a list of all block positions, for blocks matching the filter.
This will scan in a square with length 2*range + 1. So range = 0 for example will only scan the chunk the player
is standing in, while range = 1 will scan in a 3x3 area.

		Args:
			chunkRange: the range to scan around the center chunk 

		Returns:
			a list of all matching block positions. 
		"""
		pass

	@overload
	def scanChunkRange(self, centerX: int, centerZ: int, chunkrange: int) -> List[Pos3D]:
		"""Scans all chunks in the given range around the center chunk and returns a list of all block positions, for blocks matching the filter.
This will scan in a square with length 2*range + 1. So range = 0 for example will only scan the specified chunk,
while range = 1 will scan in a 3x3 area.

		Args:
			centerZ: the z coordinate of the center chunk to scan around 
			centerX: the x coordinate of the center chunk to scan around 
			chunkrange: the range to scan around the center chunk 

		Returns:
			a list of all matching block positions. 
		"""
		pass

	@overload
	def getBlocksInChunk(self, chunkX: int, chunkZ: int, ignoreState: bool) -> Mapping[str, int]:
		"""Gets the amount of all blocks matching the criteria inside the chunk.

		Args:
			ignoreState: whether multiple states should be combined to a single block 
			chunkX: the x coordinate of the chunk to scan 
			chunkZ: the z coordinate of the chunk to scan 

		Returns:
			a map of all blocks inside the specified chunk and their respective count. 
		"""
		pass

	@overload
	def getBlocksInChunks(self, centerX: int, centerZ: int, chunkRange: int, ignoreState: bool) -> Mapping[str, int]:
		"""Gets the amount of all blocks matching the criteria inside a square around the player.

		Args:
			chunkRange: the range to scan around the center chunk 
			centerZ: the z coordinate of the center chunk to scan around 
			ignoreState: whether multiple states should be combined to a single block 
			centerX: the x coordinate of the center chunk to scan around 

		Returns:
			a map of all blocks inside the specified chunks and their respective count. 
		"""
		pass

	@overload
	def getCachedAmount(self) -> int:
		"""Get the amount of cached block states. This will normally be around 200 - 400.

		Returns:
			the amount of cached block states. 
		"""
		pass

	pass


