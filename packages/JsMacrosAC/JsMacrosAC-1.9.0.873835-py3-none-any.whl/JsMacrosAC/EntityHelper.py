from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .BaseHelper import BaseHelper
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .Pos2D import Pos2D
from .TextHelper import TextHelper
from .BlockDataHelper import BlockDataHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper
from .DirectionHelper import DirectionHelper
from .ChunkHelper import ChunkHelper
from .ClientPlayerEntityHelper import ClientPlayerEntityHelper
from .PlayerEntityHelper import PlayerEntityHelper
from .VillagerEntityHelper import VillagerEntityHelper
from .MerchantEntityHelper import MerchantEntityHelper
from .LivingEntityHelper import LivingEntityHelper
from .ItemEntityHelper import ItemEntityHelper

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

T = TypeVar("T")

class EntityHelper(Generic[T], BaseHelper):
	"""
	"""

	@overload
	def getPos(self) -> Pos3D:
		"""

		Returns:
			entity position. 
		"""
		pass

	@overload
	def getBlockPos(self) -> BlockPosHelper:
		"""
		Since: 1.6.5 

		Returns:
			entity block position. 
		"""
		pass

	@overload
	def getEyePos(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the entity's eye position. 
		"""
		pass

	@overload
	def getChunkPos(self) -> Pos2D:
		"""
		Since: 1.6.5 

		Returns:
			entity chunk coordinates. Since Pos2D only has x and y fields, z coord is y. 
		"""
		pass

	@overload
	def getX(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'x' value of the entity. 
		"""
		pass

	@overload
	def getY(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'y' value of the entity. 
		"""
		pass

	@overload
	def getZ(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'z' value of the entity. 
		"""
		pass

	@overload
	def getEyeHeight(self) -> float:
		"""
		Since: 1.2.8 

		Returns:
			the current eye height offset for the entity. 
		"""
		pass

	@overload
	def getPitch(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'pitch' value of the entity. 
		"""
		pass

	@overload
	def getYaw(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'yaw' value of the entity. 
		"""
		pass

	@overload
	def getName(self) -> TextHelper:
		"""
		Since: 1.0.8 [citation needed], returned string until 1.6.4 

		Returns:
			the name of the entity. 
		"""
		pass

	@overload
	def getType(self) -> str:
		"""

		Returns:
			the type of the entity. 
		"""
		pass

	@overload
	def isGlowing(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity has the glowing effect. 
		"""
		pass

	@overload
	def isInLava(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity is in lava. 
		"""
		pass

	@overload
	def isOnFire(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity is on fire. 
		"""
		pass

	@overload
	def isSneaking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is sneaking, 'false' otherwise. 
		"""
		pass

	@overload
	def isSprinting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is sprinting, 'false' otherwise. 
		"""
		pass

	@overload
	def getVehicle(self) -> "EntityHelper":
		"""
		Since: 1.1.8 [citation needed] 

		Returns:
			the vehicle of the entity. 
		"""
		pass

	@overload
	def rayTraceBlock(self, distance: float, fluid: bool) -> BlockDataHelper:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def rayTraceEntity(self, distance: int) -> "EntityHelper":
		"""
		Since: 1.9.0 

		Args:
			distance: 
		"""
		pass

	@overload
	def getPassengers(self) -> List["EntityHelper"]:
		"""
		Since: 1.1.8 [citation needed] 

		Returns:
			the entity passengers. 
		"""
		pass

	@overload
	def getNBT(self) -> NBTElementHelper_NBTCompoundHelper:
		"""
		Since: 1.2.8, was a String until 1.5.0 
		"""
		pass

	@overload
	def setCustomName(self, name: TextHelper) -> "EntityHelper":
		"""
		Since: 1.6.4 

		Args:
			name: 
		"""
		pass

	@overload
	def setCustomNameVisible(self, b: bool) -> "EntityHelper":
		"""sets the name to always display\n
		Since: 1.8.0 

		Args:
			b: 
		"""
		pass

	@overload
	def setGlowingColor(self, color: int) -> "EntityHelper":
		"""

		Args:
			color: 
		"""
		pass

	@overload
	def resetGlowingColor(self) -> "EntityHelper":
		"""
		"""
		pass

	@overload
	def getGlowingColor(self) -> int:
		"""warning: affected by setGlowingColor\n
		Since: 1.8.2 

		Returns:
			glow color 
		"""
		pass

	@overload
	def setGlowing(self, val: bool) -> "EntityHelper":
		"""Sets whether the entity is glowing.\n
		Since: 1.1.9 

		Args:
			val: 
		"""
		pass

	@overload
	def resetGlowing(self) -> "EntityHelper":
		"""reset the glowing effect to proper value.\n
		Since: 1.6.3 
		"""
		pass

	@overload
	def isAlive(self) -> bool:
		"""Checks if the entity is still alive.\n
		Since: 1.2.8 
		"""
		pass

	@overload
	def getUUID(self) -> str:
		"""
		Since: 1.6.5 

		Returns:
			UUID of the entity, random* if not a player, otherwise the player's uuid. 
		"""
		pass

	@overload
	def getMaxAir(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the maximum amount of air this entity can have. 
		"""
		pass

	@overload
	def getAir(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the amount of air this entity has. 
		"""
		pass

	@overload
	def getSpeed(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			this entity's current speed in blocks per second. 
		"""
		pass

	@overload
	def getFacingDirection(self) -> DirectionHelper:
		"""
		Since: 1.8.4 

		Returns:
			the direction the entity is facing, rounded to the nearest 45 degrees. 
		"""
		pass

	@overload
	def distanceTo(self, entity: "EntityHelper") -> float:
		"""
		Since: 1.8.4 

		Returns:
			the distance between this entity and the specified one. 
		"""
		pass

	@overload
	def distanceTo(self, pos: BlockPosHelper) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the distance between this entity and the specified position. 
		"""
		pass

	@overload
	def distanceTo(self, pos: Pos3D) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the distance between this entity and the specified position. 
		"""
		pass

	@overload
	def distanceTo(self, x: float, y: float, z: float) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the distance between this entity and the specified position. 
		"""
		pass

	@overload
	def getVelocity(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the velocity vector. 
		"""
		pass

	@overload
	def getChunk(self) -> ChunkHelper:
		"""
		Since: 1.8.4 

		Returns:
			the chunk helper for the chunk this entity is in. 
		"""
		pass

	@overload
	def getBiome(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the biome this entity is in. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def create(self, e: Entity) -> "EntityHelper":
		"""mostly for internal use.

		Args:
			e: mc entity. 

		Returns:
			correct subclass of this. 
		"""
		pass

	@overload
	def asClientPlayer(self) -> ClientPlayerEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asPlayer(self) -> PlayerEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asVillager(self) -> VillagerEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asMerchant(self) -> MerchantEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asLiving(self) -> LivingEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asAnimal(self) -> LivingEntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			this helper as an animal entity helper (mainly for typescript). 
		"""
		pass

	@overload
	def asItem(self) -> ItemEntityHelper:
		"""
		Since: 1.6.3 

		Returns:
			cast of this entity helper (mainly for typescript) 
		"""
		pass

	@overload
	def asServerEntity(self) -> "EntityHelper":
		"""
		Since: 1.8.4 

		Returns:
			the entity as a server entity if an integrated server is running and 'null' otherwise. 
		"""
		pass

	pass


