from typing import overload
from typing import List
from typing import TypeVar
from typing import Any
from .BaseHelper import BaseHelper
from .BlockPosHelper import BlockPosHelper
from .MethodWrapper import MethodWrapper

net_minecraft_world_Heightmap = TypeVar("net_minecraft_world_Heightmap")
Heightmap = net_minecraft_world_Heightmap

java_util_Map_Entry_net_minecraft_world_Heightmap_Type,net_minecraft_world_Heightmap_ = TypeVar("java_util_Map_Entry_net_minecraft_world_Heightmap_Type,net_minecraft_world_Heightmap_")
Map_Entry = java_util_Map_Entry_net_minecraft_world_Heightmap_Type,net_minecraft_world_Heightmap_

net_minecraft_world_chunk_Chunk = TypeVar("net_minecraft_world_chunk_Chunk")
Chunk = net_minecraft_world_chunk_Chunk


class ChunkHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: Chunk) -> None:
		pass

	@overload
	def getStartingBlock(self) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Returns:
			the first block (0 0 0 coordinate) of this chunk. 
		"""
		pass

	@overload
	def getOffsetBlock(self, xOffset: int, y: int, zOffset: int) -> BlockPosHelper:
		"""The coordinates are relative to the starting chunk position, see ChunkHelper#getStartingBlock() .\n
		Since: 1.8.4 

		Args:
			xOffset: the xOffset offset 
			y: the actual y coordinate 
			zOffset: the zOffset offset 

		Returns:
			the block offset from the starting block of this chunk by xOffset y zOffset. 
		"""
		pass

	@overload
	def getMaxBuildHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum height of this chunk. 
		"""
		pass

	@overload
	def getMinBuildHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the minimum height of this chunk. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this chunk. 
		"""
		pass

	@overload
	def getTopYAt(self, xOffset: int, zOffset: int, heightmap: Heightmap) -> int:
		"""
		Since: 1.8.4 

		Args:
			heightmap: the heightmap to use 
			xOffset: the xOffset coordinate 
			zOffset: the zOffset coordinate 

		Returns:
			the maximum 'y' position of all blocks inside this chunk. 
		"""
		pass

	@overload
	def getChunkX(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the 'x' coordinate (not the world coordinate) of this chunk. 
		"""
		pass

	@overload
	def getChunkZ(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the 'z' coordinate (not the world coordinate) of this chunk. 
		"""
		pass

	@overload
	def getBiome(self, xOffset: int, y: int, zOffset: int) -> str:
		"""
		Since: 1.8.4 

		Args:
			xOffset: the x offset 
			y: the y coordinate 
			zOffset: the z offset 

		Returns:
			the biome at the given position. 
		"""
		pass

	@overload
	def getInhabitedTime(self) -> float:
		"""With an increasing inhabited time, the local difficulty increases and stronger mobs will
spawn. Because the time is cumulative, the more players are in the chunk, the faster the time
will increase.\n
		Since: 1.8.4 

		Returns:
			the cumulative time players have spent inside this chunk. 
		"""
		pass

	@overload
	def getEntities(self) -> List[Any]:
		"""
		Since: 1.8.4 

		Returns:
			all entities inside this chunk. 
		"""
		pass

	@overload
	def getTileEntities(self) -> List[BlockPosHelper]:
		"""
		Since: 1.8.4 

		Returns:
			all tile entity positions inside this chunk. 
		"""
		pass

	@overload
	def forEach(self, includeAir: bool, callback: MethodWrapper) -> "ChunkHelper":
		"""
		Since: 1.8.4 

		Args:
			includeAir: whether to include air blocks or not 
			callback: the callback function 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def containsAny(self, blocks: List[str]) -> bool:
		"""
		Since: 1.8.4 

		Args:
			blocks: the blocks to search for 

		Returns:
			'true' if this chunk contains at least one of the specified blocks, 'false' otherwise. 
		"""
		pass

	@overload
	def containsAll(self, blocks: List[str]) -> bool:
		"""
		Since: 1.8.4 

		Args:
			blocks: the blocks to search for 

		Returns:
			'true' if the chunk contains all the specified blocks, 'false' otherwise. 
		"""
		pass

	@overload
	def getHeightmaps(self) -> List[Map_Entry]:
		"""
		Since: 1.8.4 

		Returns:
			a map of the raw heightmap data. 
		"""
		pass

	@overload
	def getSurfaceHeightmap(self) -> Heightmap:
		"""
		Since: 1.8.4 

		Returns:
			the raw surface heightmap. 
		"""
		pass

	@overload
	def getOceanFloorHeightmap(self) -> Heightmap:
		"""
		Since: 1.8.4 

		Returns:
			the raw ocean floor heightmap. 
		"""
		pass

	@overload
	def getMotionBlockingHeightmap(self) -> Heightmap:
		"""
		Since: 1.8.4 

		Returns:
			the raw motion blocking heightmap. 
		"""
		pass

	@overload
	def getMotionBlockingNoLeavesHeightmap(self) -> Heightmap:
		"""
		Since: 1.8.4 

		Returns:
			the raw motion blocking heightmap without leaves. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


