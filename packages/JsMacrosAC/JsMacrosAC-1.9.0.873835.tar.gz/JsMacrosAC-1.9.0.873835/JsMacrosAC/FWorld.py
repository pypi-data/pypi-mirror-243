from typing import overload
from typing import List
from typing import Mapping
from .BaseLibrary import BaseLibrary
from .PlayerEntityHelper import PlayerEntityHelper
from .PlayerListEntryHelper import PlayerListEntryHelper
from .BlockDataHelper import BlockDataHelper
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .ChunkHelper import ChunkHelper
from .WorldScannerBuilder import WorldScannerBuilder
from .MethodWrapper import MethodWrapper
from .WorldScanner import WorldScanner
from .ScoreboardsHelper import ScoreboardsHelper
from .EntityHelper import EntityHelper
from .BossBarHelper import BossBarHelper
from .TextHelper import TextHelper


class FWorld(BaseLibrary):
	"""Functions for getting and using world data. 
An instance of this class is passed to scripts as the 'World' variable.
	"""
	serverInstantTPS: float
	server1MAverageTPS: float
	server5MAverageTPS: float
	server15MAverageTPS: float

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def isWorldLoaded(self) -> bool:
		"""returns whether a world is currently loaded\n
		Since: 1.3.0 
		"""
		pass

	@overload
	def getLoadedPlayers(self) -> List[PlayerEntityHelper]:
		"""

		Returns:
			players within render distance. 
		"""
		pass

	@overload
	def getPlayers(self) -> List[PlayerListEntryHelper]:
		"""

		Returns:
			players on the tablist. 
		"""
		pass

	@overload
	def getPlayerEntry(self, name: str) -> PlayerListEntryHelper:
		"""
		Since: 1.8.4 

		Args:
			name: the name of the player to get the entry for 

		Returns:
			player entry for the given player's name or 'null' if not found. 
		"""
		pass

	@overload
	def getBlock(self, x: int, y: int, z: int) -> BlockDataHelper:
		"""

		Args:
			x: 
			y: 
			z: 

		Returns:
			The block at that position. 
		"""
		pass

	@overload
	def getBlock(self, pos: Pos3D) -> BlockDataHelper:
		pass

	@overload
	def getBlock(self, pos: BlockPosHelper) -> BlockDataHelper:
		pass

	@overload
	def getChunk(self, x: int, z: int) -> ChunkHelper:
		"""The x and z position of the chunk can be calculated by the following formula: xChunk =
x >> 4; zChunk = z >> 4;\n
		Since: 1.8.4 

		Args:
			x: the x coordinate of the chunk, not the absolute position 
			z: the z coordinate of the chunk, not the absolute position 

		Returns:
			ChunkHelper for the chunk coordinates ChunkHelper . 
		"""
		pass

	@overload
	def getWorldScanner(self) -> WorldScannerBuilder:
		"""Usage: This will return all blocks that are facing south, don't require a tool to break,
have a hardness of 10 or less and whose name contains either chest or barrel. World.getWorldScanner()
    .withBlockFilter("getHardness").is(" =", 10)
    .andStringBlockFilter().contains("chest", "barrel")
    .withStringStateFilter().contains("facing=south")
    .andStateFilter("isToolRequired").is(false)
    .build()\n
		Since: 1.6.5 

		Returns:
			a builder to create a WorldScanner. 
		"""
		pass

	@overload
	def getWorldScanner(self, blockFilter: MethodWrapper, stateFilter: MethodWrapper) -> WorldScanner:
		"""
		Since: 1.6.5 

		Returns:
			a scanner for the current world. 
		"""
		pass

	@overload
	def findBlocksMatching(self, centerX: int, centerZ: int, id: str, chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			chunkrange: 
			id: 
		"""
		pass

	@overload
	def findBlocksMatching(self, id: str, chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			chunkrange: 
			id: 
		"""
		pass

	@overload
	def findBlocksMatching(self, ids: List[str], chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			chunkrange: 
			ids: 
		"""
		pass

	@overload
	def findBlocksMatching(self, centerX: int, centerZ: int, ids: List[str], chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			centerZ: 
			centerX: 
			chunkrange: 
			ids: 
		"""
		pass

	@overload
	def findBlocksMatching(self, blockFilter: MethodWrapper, stateFilter: MethodWrapper, chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			blockFilter: 
			stateFilter: 
			chunkrange: 
		"""
		pass

	@overload
	def findBlocksMatching(self, chunkX: int, chunkZ: int, blockFilter: MethodWrapper, stateFilter: MethodWrapper, chunkrange: int) -> List[Pos3D]:
		"""
		Since: 1.6.4 

		Args:
			blockFilter: 
			stateFilter: 
			chunkrange: 
			chunkX: 
			chunkZ: 
		"""
		pass

	@overload
	def iterateSphere(self, pos: BlockPosHelper, radius: int, callback: MethodWrapper) -> None:
		"""By default, air blocks are ignored and the callback is only called for real blocks.\n
		Since: 1.8.4 

		Args:
			pos: the center position 
			callback: the callback to call for each block 
			radius: the radius to scan 
		"""
		pass

	@overload
	def iterateSphere(self, pos: BlockPosHelper, radius: int, ignoreAir: bool, callback: MethodWrapper) -> None:
		"""
		Since: 1.8.4 

		Args:
			pos: the center position 
			callback: the callback to call for each block 
			radius: the radius to scan 
			ignoreAir: whether to ignore air blocks 
		"""
		pass

	@overload
	def iterateBox(self, pos1: BlockPosHelper, pos2: BlockPosHelper, callback: MethodWrapper) -> None:
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position 
			callback: the callback to call for each block 
			pos2: the second position 
		"""
		pass

	@overload
	def iterateBox(self, pos1: BlockPosHelper, pos2: BlockPosHelper, ignoreAir: bool, callback: MethodWrapper) -> None:
		"""
		Since: 1.8.4 

		Args:
			pos1: the first position 
			callback: the callback to call for each block 
			pos2: the second position 
			ignoreAir: whether to ignore air blocks 
		"""
		pass

	@overload
	def getScoreboards(self) -> ScoreboardsHelper:
		"""
		Since: 1.2.9 

		Returns:
			a helper for the scoreboards provided to the client. 
		"""
		pass

	@overload
	def getEntities(self) -> List[EntityHelper]:
		"""

		Returns:
			all entities in the render distance. 
		"""
		pass

	@overload
	def getEntities(self, types: List[str]) -> List[EntityHelper]:
		"""
		Since: 1.8.4 

		Args:
			types: the entity types to consider 

		Returns:
			all entities in the render distance, that match the specified entity type. 
		"""
		pass

	@overload
	def getEntities(self, distance: float) -> List[EntityHelper]:
		"""
		Since: 1.8.4 

		Args:
			distance: the maximum distance to search for entities 

		Returns:
			a list of entities within the specified distance to the player. 
		"""
		pass

	@overload
	def getEntities(self, distance: float, types: List[str]) -> List[EntityHelper]:
		"""
		Since: 1.8.4 

		Args:
			types: the entity types to consider 
			distance: the maximum distance to search for entities 

		Returns:
			a list of entities within the specified distance to the player, that match the specified entity type. 
		"""
		pass

	@overload
	def getEntities(self, filter: MethodWrapper) -> List[EntityHelper]:
		"""
		Since: 1.8.4 

		Args:
			filter: the entity filter 

		Returns:
			a list of entities that match the specified filter. 
		"""
		pass

	@overload
	def rayTraceBlock(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, fluid: bool) -> BlockDataHelper:
		"""raytrace between two points returning the first block hit.\n
		Since: 1.6.5 

		Args:
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
			fluid: 
		"""
		pass

	@overload
	def rayTraceEntity(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> EntityHelper:
		"""raytrace between two points returning the first entity hit.\n
		Since: 1.8.3 

		Args:
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def getDimension(self) -> str:
		"""
		Since: 1.1.2 

		Returns:
			the current dimension. 
		"""
		pass

	@overload
	def getBiome(self) -> str:
		"""
		Since: 1.1.5 

		Returns:
			the current biome. 
		"""
		pass

	@overload
	def getTime(self) -> float:
		"""ticks processed since world was started.\n
		Since: 1.1.5 

		Returns:
			the current world time. 
		"""
		pass

	@overload
	def getTimeOfDay(self) -> float:
		"""ticks passed since world was started INCLUDING those skipped when nights were cut short with sleeping.\n
		Since: 1.1.5 

		Returns:
			the current world time of day. 
		"""
		pass

	@overload
	def isDay(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if it is daytime, 'false' otherwise. 
		"""
		pass

	@overload
	def isNight(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if it is nighttime, 'false' otherwise. 
		"""
		pass

	@overload
	def isRaining(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if it is raining, 'false' otherwise. 
		"""
		pass

	@overload
	def isThundering(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if it is thundering, 'false' otherwise. 
		"""
		pass

	@overload
	def getWorldIdentifier(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			an identifier for the loaded world that is based on the world's name or server ip and
thus most likely unique enough to identify a specific world, or '"UNKNOWN_NAME"' if no world was found. 
		"""
		pass

	@overload
	def getRespawnPos(self) -> BlockPosHelper:
		"""
		Since: 1.2.6 

		Returns:
			respawn position. 
		"""
		pass

	@overload
	def getDifficulty(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			world difficulty as an Integer . 
		"""
		pass

	@overload
	def getMoonPhase(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			moon phase as an Integer . 
		"""
		pass

	@overload
	def getSkyLight(self, x: int, y: int, z: int) -> int:
		"""
		Since: 1.1.2 

		Args:
			x: 
			y: 
			z: 

		Returns:
			sky light as an Integer . 
		"""
		pass

	@overload
	def getBlockLight(self, x: int, y: int, z: int) -> int:
		"""
		Since: 1.1.2 

		Args:
			x: 
			y: 
			z: 

		Returns:
			block light as an Integer . 
		"""
		pass

	@overload
	def playSoundFile(self, file: str, volume: float) -> Clip:
		"""plays a sound file using javax's sound stuff.\n
		Since: 1.1.7 

		Args:
			volume: 
			file: 
		"""
		pass

	@overload
	def playSound(self, id: str) -> None:
		"""
		Since: 1.1.7 

		Args:
			id: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float) -> None:
		"""
		Since: 1.1.7 

		Args:
			volume: 
			id: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float) -> None:
		"""
		Since: 1.1.7 

		Args:
			volume: 
			id: 
			pitch: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		"""plays a minecraft sound using the internal system.\n
		Since: 1.1.7 

		Args:
			volume: 
			x: 
			y: 
			z: 
			id: 
			pitch: 
		"""
		pass

	@overload
	def getBossBars(self) -> Mapping[str, BossBarHelper]:
		"""
		Since: 1.2.1 

		Returns:
			a map of boss bars by the boss bar's UUID. 
		"""
		pass

	@overload
	def isChunkLoaded(self, chunkX: int, chunkZ: int) -> bool:
		"""Check whether a chunk is within the render distance and loaded.\n
		Since: 1.2.2 

		Args:
			chunkX: 
			chunkZ: 
		"""
		pass

	@overload
	def getCurrentServerAddress(self) -> str:
		"""
		Since: 1.2.2 

		Returns:
			the current server address as a string ( 'server.address/server.ip:port' ). 
		"""
		pass

	@overload
	def getBiomeAt(self, x: int, z: int) -> str:
		"""
		Since: 1.2.2 [Citation Needed] 

		Args:
			x: 
			z: 

		Returns:
			biome at specified location, only works if the block/chunk is loaded. 
		"""
		pass

	@overload
	def getBiomeAt(self, x: int, y: int, z: int) -> str:
		"""
		Since: 1.8.4 

		Args:
			x: 
			y: 
			z: 

		Returns:
			biome at specified location, only works if the block/chunk is loaded. 
		"""
		pass

	@overload
	def getServerTPS(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps with various timings. 
		"""
		pass

	@overload
	def getTabListHeader(self) -> TextHelper:
		"""
		Since: 1.3.1 

		Returns:
			text helper for the top part of the tab list (above the players) 
		"""
		pass

	@overload
	def getTabListFooter(self) -> TextHelper:
		"""
		Since: 1.3.1 

		Returns:
			text helper for the bottom part of the tab list (below the players) 
		"""
		pass

	@overload
	def spawnParticle(self, id: str, x: float, y: float, z: float, count: int) -> None:
		"""Summons the amount of particles at the desired position.\n
		Since: 1.8.4 

		Args:
			x: the x position to spawn the particle 
			count: the amount of particles to spawn 
			y: the y position to spawn the particle 
			z: the z position to spawn the particle 
			id: the particle id 
		"""
		pass

	@overload
	def spawnParticle(self, id: str, x: float, y: float, z: float, deltaX: float, deltaY: float, deltaZ: float, speed: float, count: int, force: bool) -> None:
		"""Summons the amount of particles at the desired position with some variation of delta and the
given speed.\n
		Since: 1.8.4 

		Args:
			deltaZ: the z variation of the particle 
			deltaX: the x variation of the particle 
			deltaY: the y variation of the particle 
			x: the x position to spawn the particle 
			count: the amount of particles to spawn 
			y: the y position to spawn the particle 
			z: the z position to spawn the particle 
			force: whether to show the particle if it's more than 32 blocks away 
			id: the particle id 
			speed: the speed of the particle 
		"""
		pass

	@overload
	def getServerInstantTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps. 
		"""
		pass

	@overload
	def getServer1MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 1 minute average. 
		"""
		pass

	@overload
	def getServer5MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 5 minute average. 
		"""
		pass

	@overload
	def getServer15MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 15 minute average. 
		"""
		pass

	pass


