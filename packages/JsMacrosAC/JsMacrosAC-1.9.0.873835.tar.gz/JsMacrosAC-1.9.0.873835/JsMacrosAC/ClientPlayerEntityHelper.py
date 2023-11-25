from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .PlayerEntityHelper import PlayerEntityHelper
from .Pos3D import Pos3D
from .BlockPosHelper import BlockPosHelper
from .EntityHelper import EntityHelper
from .AdvancementManagerHelper import AdvancementManagerHelper
from .BlockStateHelper import BlockStateHelper
from .ItemStackHelper import ItemStackHelper

T = TypeVar("T")

class ClientPlayerEntityHelper(Generic[T], PlayerEntityHelper):
	"""
	Since: 1.0.3 
	"""

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def setVelocity(self, velocity: Pos3D) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def setVelocity(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def addVelocity(self, velocity: Pos3D) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def addVelocity(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def setPos(self, pos: Pos3D) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def setPos(self, pos: Pos3D, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def setPos(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def setPos(self, x: float, y: float, z: float, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addPos(self, pos: Pos3D) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def addPos(self, pos: Pos3D, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addPos(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def addPos(self, x: float, y: float, z: float, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def lookAt(self, direction: str) -> "ClientPlayerEntityHelper":
		"""Sets the player rotation along the given axis and keeps the other axis the same.\n
		Since: 1.8.4 

		Args:
			direction: possible values are "up", "down", "north", "south", "east", "west" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def lookAt(self, yaw: float, pitch: float) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.0.3 

		Args:
			pitch: (was yaw prior to 1.2.6) 
			yaw: (was pitch prior to 1.2.6) 
		"""
		pass

	@overload
	def lookAt(self, x: float, y: float, z: float) -> "ClientPlayerEntityHelper":
		"""look at the specified coordinates.\n
		Since: 1.2.8 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def tryLookAt(self, x: int, y: int, z: int) -> bool:
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the block to look at 
			y: the y coordinate of the block to look at 
			z: the z coordinate of the block to look at 

		Returns:
			'true' if the player is targeting the specified block, 'false' otherwise. 
		"""
		pass

	@overload
	def tryLookAt(self, pos: BlockPosHelper) -> bool:
		"""Will try many rotations to find one that will make the player target the specified block. If
successful, the player will be turned towards the block and 'true' will be returned. If 'false' is returned, the player will keep its current rotation.\n
		Since: 1.8.4 

		Args:
			pos: the position of the block to look at 

		Returns:
			'true' if the player is targeting the specified block, 'false' otherwise. 
		"""
		pass

	@overload
	def turnLeft(self) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def turnRight(self) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def turnBack(self) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def attack(self, entity: EntityHelper) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0 

		Args:
			entity: 
		"""
		pass

	@overload
	def attack(self, entity: EntityHelper, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			entity: 
		"""
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: str) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to attack 
			y: the y coordinate to attack 
			z: the z coordinate to attack 
			direction: possible values are "up", "down", "north", "south", "east", "west" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: int) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0 

		Args:
			x: 
			y: 
			z: 
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 
		"""
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: str, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to attack 
			await: whether to wait for the attack to finish 
			y: the y coordinate to attack 
			z: the z coordinate to attack 
			direction: possible values are "up", "down", "north", "south", "east", "west" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: int, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			x: 
			await: 
			y: 
			z: 
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 
		"""
		pass

	@overload
	def interactEntity(self, entity: EntityHelper, offHand: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			entity: 
			offHand: 
		"""
		pass

	@overload
	def interactEntity(self, entity: EntityHelper, offHand: bool, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			entity: 
			offHand: 
		"""
		pass

	@overload
	def interactItem(self, offHand: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			offHand: 
		"""
		pass

	@overload
	def interactItem(self, offHand: bool, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			offHand: 
		"""
		pass

	@overload
	def interactBlock(self, x: int, y: int, z: int, direction: str, offHand: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to interact 
			y: the y coordinate to interact 
			z: the z coordinate to interact 
			direction: possible values are "up", "down", "north", "south", "east", "west" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def interactBlock(self, x: int, y: int, z: int, direction: int, offHand: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			x: 
			y: 
			z: 
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 
			offHand: 
		"""
		pass

	@overload
	def interactBlock(self, x: int, y: int, z: int, direction: str, offHand: bool, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to interact 
			await: whether to wait for the interaction to complete 
			y: the y coordinate to interact 
			z: the z coordinate to interact 
			direction: possible values are "up", "down", "north", "south", "east", "west" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def interactBlock(self, x: int, y: int, z: int, direction: int, offHand: bool, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			x: 
			await: whether to wait for the interaction to complete 
			y: 
			z: 
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 
			offHand: 
		"""
		pass

	@overload
	def interact(self) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def interact(self, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
		"""
		pass

	@overload
	def attack(self) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def attack(self, await_: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
		"""
		pass

	@overload
	def setLongAttack(self, stop: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.3 

		Args:
			stop: 
		"""
		pass

	@overload
	def setLongInteract(self, stop: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.6.3 

		Args:
			stop: 
		"""
		pass

	@overload
	def getItemCooldownsRemainingTicks(self) -> Mapping[str, int]:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getItemCooldownRemainingTicks(self, item: str) -> int:
		"""
		Since: 1.6.5 

		Args:
			item: 
		"""
		pass

	@overload
	def getTicksSinceCooldownsStart(self) -> Mapping[str, int]:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getTicksSinceCooldownStart(self, item: str) -> int:
		"""
		Since: 1.6.5 

		Args:
			item: 
		"""
		pass

	@overload
	def getFoodLevel(self) -> int:
		"""
		Since: 1.1.2 
		"""
		pass

	@overload
	def getSaturation(self) -> float:
		"""This will return the invisible hunger decade that you may have seen in mods as a yellow overlay.\n
		Since: 1.8.4 

		Returns:
			the saturation level. 
		"""
		pass

	@overload
	def dropHeldItem(self, dropStack: bool) -> "ClientPlayerEntityHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAdvancementManager(self) -> AdvancementManagerHelper:
		"""
		Since: 1.8.4 

		Returns:
			an advancement manager to work with advancements. 
		"""
		pass

	@overload
	def calculateMiningSpeed(self, block: BlockStateHelper) -> int:
		"""The returned time is an approximation and will likely be off by a few ticks, although it
should always be less than the actual time.

		Args:
			block: the block to mine 

		Returns:
			the time in ticks that it will approximately take the player with the currently held
item to mine said block. 
		"""
		pass

	@overload
	def calculateMiningSpeed(self, usedItem: ItemStackHelper, blockState: BlockStateHelper) -> int:
		"""Calculate mining speed for a given block mined with a specified item in ticks. Use air to
calculate the mining speed for the hand. The returned time is an approximation and will
likely be off by a few ticks, although it should always be less than the actual time.\n
		Since: 1.8.4 

		Args:
			blockState: the block to mine 
			usedItem: the item to mine with 

		Returns:
			the time in ticks that it will approximately take the player with the specified item
to mine said block. 
		"""
		pass

	pass


