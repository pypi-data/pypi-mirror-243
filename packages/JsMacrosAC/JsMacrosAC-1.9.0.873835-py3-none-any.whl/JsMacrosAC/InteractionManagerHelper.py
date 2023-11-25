from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .BlockPosHelper import BlockPosHelper
from .EntityHelper import EntityHelper
from .InteractionProxy_Break_BreakBlockResult import InteractionProxy_Break_BreakBlockResult
from .MethodWrapper import MethodWrapper

net_minecraft_client_network_ClientPlayerInteractionManager = TypeVar("net_minecraft_client_network_ClientPlayerInteractionManager")
ClientPlayerInteractionManager = net_minecraft_client_network_ClientPlayerInteractionManager


class InteractionManagerHelper(BaseHelper):
	"""Helper for ClientPlayerInteractionManager
it accesses interaction manager from 'mc' instead of 'base' , to avoid issues\n
	Since: 1.9.0 
	"""
	autoUpdateBase: bool

	@overload
	def __init__(self, base: ClientPlayerInteractionManager) -> None:
		pass

	@overload
	def checkBase(self, update: bool) -> bool:
		"""checks if the base matches the current manager

		Args:
			update: true if the base should be updated. otherwise it'll raise an error if it's not up-to-date 

		Returns:
			true if base is available 
		"""
		pass

	@overload
	def getGameMode(self) -> str:
		"""
		Since: 1.9.0 

		Returns:
			the player's current gamemode. 
		"""
		pass

	@overload
	def setGameMode(self, gameMode: str) -> "InteractionManagerHelper":
		"""
		Since: 1.9.0 

		Args:
			gameMode: possible values are survival, creative, adventure, spectator (case insensitive) 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getReach(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current reach distance of the player. 
		"""
		pass

	@overload
	def setTarget(self, x: int, y: int, z: int) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, x: int, y: int, z: int, direction: str) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, x: int, y: int, z: int, direction: int) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, pos: BlockPosHelper) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, pos: BlockPosHelper, direction: str) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, pos: BlockPosHelper, direction: int) -> "InteractionManagerHelper":
		"""sets crosshair target to a block\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTarget(self, entity: EntityHelper) -> "InteractionManagerHelper":
		"""sets crosshair target to an entity\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def getTargetedBlock(self) -> BlockPosHelper:
		"""
		Since: 1.9.0 

		Returns:
			targeted block pos, null if not targeting block 
		"""
		pass

	@overload
	def getTargetedEntity(self) -> EntityHelper:
		"""
		Since: 1.9.0 

		Returns:
			targeted entity, null if not targeting entity 
		"""
		pass

	@overload
	def setTargetMissed(self) -> "InteractionManagerHelper":
		"""sets crosshair target to missed (doesn't target anything)\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def hasTargetOverride(self) -> bool:
		"""
		Since: 1.9.0 

		Returns:
			'true' if target have been set by 'ClientPlayerEntityHelper#setTarget()' or 'ClientPlayerEntityHelper#setTargetMissed()' 
		"""
		pass

	@overload
	def clearTargetOverride(self) -> "InteractionManagerHelper":
		"""clears target override\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTargetRangeCheck(self, enabled: bool, autoClear: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.9.0 

		Args:
			autoClear: if override should clear when out of range.
                 if 'false' , target will set to missed if out of range. default is 'true' 
			enabled: if target overriding should check range. default is 'true' 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTargetAirCheck(self, enabled: bool, autoClear: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.9.0 

		Args:
			autoClear: if override should clear when is air.
                 if 'false' , target will set to missed if is air. default is 'false' 
			enabled: if target overriding should check air. default is 'false' 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setTargetShapeCheck(self, enabled: bool, autoClear: bool) -> "InteractionManagerHelper":
		"""this check ignores air. use 'ClientPlayerEntityHelper#setTargetAirCheck()' to check air.\n
		Since: 1.9.0 

		Args:
			autoClear: if override should clear when shape is empty.
                 if 'false' , target will set to missed if is empty. default is 'false' 
			enabled: if target overriding should check block shape. default is 'true' 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def resetTargetChecks(self) -> "InteractionManagerHelper":
		"""resets all range, air and shape check settings to default.\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def attack(self) -> "InteractionManagerHelper":
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def attack(self, await_: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
		"""
		pass

	@overload
	def attack(self, entity: EntityHelper) -> "InteractionManagerHelper":
		"""
		Since: 1.5.0 

		Args:
			entity: 
		"""
		pass

	@overload
	def attack(self, entity: EntityHelper, await_: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			entity: 
		"""
		pass

	@overload
	def attack(self, x: int, y: int, z: int, direction: str) -> "InteractionManagerHelper":
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
	def attack(self, x: int, y: int, z: int, direction: int) -> "InteractionManagerHelper":
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
	def attack(self, x: int, y: int, z: int, direction: str, await_: bool) -> "InteractionManagerHelper":
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
	def attack(self, x: int, y: int, z: int, direction: int, await_: bool) -> "InteractionManagerHelper":
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
	def breakBlock(self) -> InteractionProxy_Break_BreakBlockResult:
		"""breaks a block, will wait till it's done you can use 'ClientPlayerEntityHelper#setTarget()' to specify which block to break\n
		Since: 1.9.0 

		Returns:
			result, or null if interaction manager is unavailable 
		"""
		pass

	@overload
	def breakBlock(self, x: int, y: int, z: int) -> InteractionProxy_Break_BreakBlockResult:
		"""breaks a block, will wait till it's done this is the same as: setTarget(x, y, z);
let res = null;
if (getTargetedBlock()?.getRaw().equals(new BlockPos(x, y, z))) res = breakBlock();
clearTargetOverride();
return res;\n
		Since: 1.9.0 

		Returns:
			result 
		"""
		pass

	@overload
	def breakBlock(self, pos: BlockPosHelper) -> InteractionProxy_Break_BreakBlockResult:
		"""breaks a block, will wait till it's done this is the same as: setTarget(pos);
let res = null;
if (getTargetedBlock()?.equals(pos)) res = breakBlock();
clearTargetOverride();
return res;\n
		Since: 1.9.0 

		Returns:
			result 
		"""
		pass

	@overload
	def breakBlockAsync(self, callback: MethodWrapper) -> "InteractionManagerHelper":
		"""starts breaking a block you can use 'ClientPlayerEntityHelper#setTarget()' to specify which block to break\n
		Since: 1.9.0 

		Args:
			callback: this will mostly be called on main thread!
                Use 'methodToJavaAsync()' instead of 'methodToJava()' to avoid errors. 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def isBreakingBlock(self) -> bool:
		"""
		Since: 1.8.0 
		"""
		pass

	@overload
	def hasBreakBlockOverride(self) -> bool:
		"""
		Since: 1.9.0 

		Returns:
			'true' if there's not finished block breaking from 'ClientPlayerEntityHelper#breakBlock()' 
		"""
		pass

	@overload
	def cancelBreakBlock(self) -> "InteractionManagerHelper":
		"""cancels breaking block that previously started by 'ClientPlayerEntityHelper#breakBlock()' or 'ClientPlayerEntityHelper#breakBlockAsync()'\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def interact(self) -> "InteractionManagerHelper":
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def interact(self, await_: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
		"""
		pass

	@overload
	def interactEntity(self, entity: EntityHelper, offHand: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			entity: 
			offHand: 
		"""
		pass

	@overload
	def interactEntity(self, entity: EntityHelper, offHand: bool, await_: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			entity: 
			offHand: 
		"""
		pass

	@overload
	def interactItem(self, offHand: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.5.0, renamed from 'interact' in 1.6.0 

		Args:
			offHand: 
		"""
		pass

	@overload
	def interactItem(self, offHand: bool, await_: bool) -> "InteractionManagerHelper":
		"""
		Since: 1.6.0 

		Args:
			await: 
			offHand: 
		"""
		pass

	@overload
	def interactBlock(self, x: int, y: int, z: int, direction: str, offHand: bool) -> "InteractionManagerHelper":
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
	def interactBlock(self, x: int, y: int, z: int, direction: int, offHand: bool) -> "InteractionManagerHelper":
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
	def interactBlock(self, x: int, y: int, z: int, direction: str, offHand: bool, await_: bool) -> "InteractionManagerHelper":
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
	def interactBlock(self, x: int, y: int, z: int, direction: int, offHand: bool, await_: bool) -> "InteractionManagerHelper":
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
	def holdInteract(self, holding: bool) -> "InteractionManagerHelper":
		"""starts/stops long interact\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def holdInteract(self, holding: bool, awaitFirstClick: bool) -> "InteractionManagerHelper":
		"""starts/stops long interact\n
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def holdInteract(self, ticks: int) -> int:
		"""interacts for specified number of ticks\n
		Since: 1.9.0 

		Returns:
			remaining ticks if the interaction was interrupted 
		"""
		pass

	@overload
	def holdInteract(self, ticks: int, stopOnPause: bool) -> int:
		"""interacts for specified number of ticks\n
		Since: 1.9.0 

		Args:
			stopOnPause: if 'false' , this interaction will not return when interrupted by pause.
                   the timer will not decrease, meaning it'll continue right after unpause and interact exact amount of ticks. 

		Returns:
			remaining ticks if the interaction was interrupted 
		"""
		pass

	@overload
	def hasInteractOverride(self) -> bool:
		"""
		Since: 1.9.0 

		Returns:
			'true' if interaction from 'ClientPlayerEntityHelper#holdInteract()' is active 
		"""
		pass

	pass


