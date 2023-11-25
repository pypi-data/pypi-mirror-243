from typing import overload
from typing import List
from typing import TypeVar
from .PlayerInput import PlayerInput

net_minecraft_entity_LivingEntity = TypeVar("net_minecraft_entity_LivingEntity")
LivingEntity = net_minecraft_entity_LivingEntity

java_lang_Iterable_net_minecraft_item_ItemStack_ = TypeVar("java_lang_Iterable_net_minecraft_item_ItemStack_")
Iterable = java_lang_Iterable_net_minecraft_item_ItemStack_

net_minecraft_entity_EquipmentSlot = TypeVar("net_minecraft_entity_EquipmentSlot")
EquipmentSlot = net_minecraft_entity_EquipmentSlot

net_minecraft_util_math_Box = TypeVar("net_minecraft_util_math_Box")
Box = net_minecraft_util_math_Box

net_minecraft_client_network_ClientPlayerEntity = TypeVar("net_minecraft_client_network_ClientPlayerEntity")
ClientPlayerEntity = net_minecraft_client_network_ClientPlayerEntity

net_minecraft_world_World = TypeVar("net_minecraft_world_World")
World = net_minecraft_world_World

net_minecraft_item_ItemStack = TypeVar("net_minecraft_item_ItemStack")
ItemStack = net_minecraft_item_ItemStack

net_minecraft_util_Arm = TypeVar("net_minecraft_util_Arm")
Arm = net_minecraft_util_Arm

net_minecraft_util_math_Vec3d = TypeVar("net_minecraft_util_math_Vec3d")
Vec3d = net_minecraft_util_math_Vec3d


class MovementDummy(LivingEntity):

	@overload
	def __init__(self, player: "MovementDummy") -> None:
		pass

	@overload
	def __init__(self, player: ClientPlayerEntity) -> None:
		pass

	@overload
	def __init__(self, world: World, pos: Vec3d, velocity: Vec3d, hitBox: Box, onGround: bool, isSprinting: bool, isSneaking: bool) -> None:
		pass

	@overload
	def getCoordsHistory(self) -> List[Vec3d]:
		pass

	@overload
	def getInputs(self) -> List[PlayerInput]:
		pass

	@overload
	def applyInput(self, input: PlayerInput) -> Vec3d:
		pass

	@overload
	def applyMovementInput(self, movementInput: Vec3d, f: float) -> Vec3d:
		"""We have to do this "inject" since the the applyClimbingSpeed() method
in LivingEntity is checking if we are a PlayerEntity, we want to apply the outcome of this check,
so this is why we need to set the y-velocity to 0.
		"""
		pass

	@overload
	def canMoveVoluntarily(self) -> bool:
		pass

	@overload
	def setSprinting(self, sprinting: bool) -> None:
		pass

	@overload
	def getMainHandStack(self) -> ItemStack:
		pass

	@overload
	def getArmorItems(self) -> Iterable:
		pass

	@overload
	def getEquippedStack(self, slot: EquipmentSlot) -> ItemStack:
		pass

	@overload
	def equipStack(self, slot: EquipmentSlot, stack: ItemStack) -> None:
		pass

	@overload
	def getMainArm(self) -> Arm:
		pass

	@overload
	def clone(self) -> "MovementDummy":
		pass

	pass


