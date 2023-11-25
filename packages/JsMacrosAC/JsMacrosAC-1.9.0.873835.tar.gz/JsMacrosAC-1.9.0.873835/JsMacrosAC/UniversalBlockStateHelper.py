from typing import overload
from typing import List
from typing import TypeVar
from .BlockStateHelper import BlockStateHelper
from .DirectionHelper import DirectionHelper

net_minecraft_block_BlockState = TypeVar("net_minecraft_block_BlockState")
BlockState = net_minecraft_block_BlockState


class UniversalBlockStateHelper(BlockStateHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BlockState) -> None:
		pass

	@overload
	def getAttachment(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getEastWallShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getNorthWallShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getSouthWallShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getWestWallShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getEastWireConnection(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getNorthWireConnection(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getSouthWireConnection(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getWestWireConnection(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getBlockHalf(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getDoubleBlockHalf(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getRailShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getStraightRailShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getOrientation(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getHorizontalAxis(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getAxis(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getHorizontalFacing(self) -> DirectionHelper:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getHopperFacing(self) -> DirectionHelper:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getFacing(self) -> DirectionHelper:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isUp(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isDown(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isNorth(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSouth(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isEast(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isWest(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getHoneyLevel(self) -> int:
		"""Used on beehives.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isBottom(self) -> bool:
		"""Used on scaffolding.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isBubbleColumnDown(self) -> bool:
		"""Used on bubble columns.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isBubbleColumnUp(self) -> bool:
		"""Used on bubble columns.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isAttached(self) -> bool:
		"""Used on trip wire hooks.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isDisarmed(self) -> bool:
		"""Used on trip wires.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isConditional(self) -> bool:
		"""Used on command blocks.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isEnabled(self) -> bool:
		"""Used on hoppers.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isExtended(self) -> bool:
		"""Used on pistons.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isShort(self) -> bool:
		"""Used on piston heads.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasEye(self) -> bool:
		"""Used on end portal frames.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isFalling(self) -> bool:
		"""Used on fluids.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getLevel(self) -> int:
		"""Used on fluids and stuff\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMaxLevel(self) -> int:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMinLevel(self) -> int:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isHanging(self) -> bool:
		"""Used on lanterns.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasBottle0(self) -> bool:
		"""Used on brewing stands.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasBottle1(self) -> bool:
		"""Used on brewing stands.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasBottle2(self) -> bool:
		"""Used on brewing stands.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasRecord(self) -> bool:
		"""Used on jukeboxes.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasBook(self) -> bool:
		"""Used on lecterns.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isInverted(self) -> bool:
		"""Used on daylight sensors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isInWall(self) -> bool:
		"""Used on fence gates.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isOpen(self) -> bool:
		"""Used on fence gates, barrels, trap doors and doors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isLit(self) -> bool:
		"""Used on candles, all types of furnaces, campfires and redstone torches.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isLocked(self) -> bool:
		"""Used on repeaters.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getDelay(self) -> int:
		"""Used on repeaters.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isOccupied(self) -> bool:
		"""Used on beds.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isPersistent(self) -> bool:
		"""Used on leaves.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getDistance(self) -> int:
		"""Used on leaves and scaffold.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMaxDistance(self) -> int:
		"""Used on leaves and scaffold.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMinDistance(self) -> int:
		"""Used on leaves and scaffold.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isPowered(self) -> bool:
		"""Used on bells, buttons, detector rails, diodes, doors, fence gates, lecterns, levers,
lightning rods, note blocks, observers, powered rails, pressure plates, trap doors, trip wire
hooks and trip wires.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSignalFire(self) -> bool:
		"""Used on campfires.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSnowy(self) -> bool:
		"""Used on snowy dirt blocks.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isTriggered(self) -> bool:
		"""Used on dispensers.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isUnstable(self) -> bool:
		"""Used on tnt.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isWaterlogged(self) -> bool:
		"""Used on amethysts, corals, rails, dripleaves, dripleaf stems, campfires, candles, chains,
chests, conduits, fences, double plants, ender chests, iron bars, glass panes, glow lichen,
hanging roots, ladders, lanterns, light blocks, lightning rods, pointed dripstone,
scaffolding , sculk sensors, sea pickles, signs, stairs, slabs, trap doors and walls\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getBedPart(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getDoorHinge(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getInstrument(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getPistonType(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getSlabType(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getStairShape(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getStructureBlockMode(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getBambooLeaves(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getTilt(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getVerticalDirection(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getThickness(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getChestType(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getComparatorMode(self) -> str:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def hasBerries(self) -> bool:
		"""Used on cave vine roots.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getAge(self) -> int:
		"""crop age and such\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMaxAge(self) -> int:
		pass

	@overload
	def getBites(self) -> int:
		"""Used on cakes.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getCandles(self) -> int:
		"""Used on candles.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getEggs(self) -> int:
		"""Used on turtle eggs.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getHatched(self) -> int:
		"""Used on turtle eggs.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getLayers(self) -> int:
		"""Used on snow layers.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getMoisture(self) -> int:
		"""Used on farmland.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getNote(self) -> int:
		"""Used on note blocks.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getPickles(self) -> int:
		"""Used on sea pickles.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getPower(self) -> int:
		"""Used on daylight sensors, redstone wires, sculk sensors, target blocks, weighted pressure
plates.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getStage(self) -> int:
		"""Used on bamboo, saplings.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getCharges(self) -> int:
		"""Used on respawn anchors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isShrieking(self) -> bool:
		"""Used on sculk sensors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def canSummon(self) -> bool:
		"""Used on sculk sensors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getSculkSensorPhase(self) -> str:
		"""Used on sculk sensors.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def isBloom(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getRotation(self) -> int:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot0Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot1Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot2Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot3Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot4Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def isSlot5Occupied(self) -> bool:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getFlowerAmount(self) -> int:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def getBlockFace(self) -> str:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def getDusted(self) -> int:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def isCracked(self) -> bool:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def main(self, args: List[str]) -> None:
		pass

	pass


