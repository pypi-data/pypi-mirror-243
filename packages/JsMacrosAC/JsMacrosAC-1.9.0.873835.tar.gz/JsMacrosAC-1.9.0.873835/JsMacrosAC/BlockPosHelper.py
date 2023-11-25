from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .EntityHelper import EntityHelper
from .Pos3D import Pos3D

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos


class BlockPosHelper(BaseHelper):
	"""
	Since: 1.2.6 
	"""

	@overload
	def __init__(self, b: BlockPos) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, z: int) -> None:
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'x' value of the block. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'y' value of the block. 
		"""
		pass

	@overload
	def getZ(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'z' value of the block. 
		"""
		pass

	@overload
	def up(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block above. 
		"""
		pass

	@overload
	def up(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move up 

		Returns:
			the block n-th block above. 
		"""
		pass

	@overload
	def down(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block below. 
		"""
		pass

	@overload
	def down(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move down 

		Returns:
			the block n-th block below. 
		"""
		pass

	@overload
	def north(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block to the north. 
		"""
		pass

	@overload
	def north(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move north 

		Returns:
			the n-th block to the north. 
		"""
		pass

	@overload
	def south(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block to the south. 
		"""
		pass

	@overload
	def south(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move south 

		Returns:
			the n-th block to the south. 
		"""
		pass

	@overload
	def east(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block to the east. 
		"""
		pass

	@overload
	def east(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move east 

		Returns:
			the n-th block to the east. 
		"""
		pass

	@overload
	def west(self) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Returns:
			the block to the west. 
		"""
		pass

	@overload
	def west(self, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move west 

		Returns:
			the n-th block to the west. 
		"""
		pass

	@overload
	def offset(self, direction: str) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 

		Returns:
			the block offset by the given direction. 
		"""
		pass

	@overload
	def offset(self, direction: str, distance: int) -> "BlockPosHelper":
		"""
		Since: 1.6.5 

		Args:
			distance: the distance to move in the given direction 
			direction: 0-5 in order: [DOWN, UP, NORTH, SOUTH, WEST, EAST]; 

		Returns:
			the n-th block offset by the given direction. 
		"""
		pass

	@overload
	def offset(self, x: int, y: int, z: int) -> "BlockPosHelper":
		"""
		Since: 1.8.4 

		Args:
			x: the x offset 
			y: the y offset 
			z: the y offset 

		Returns:
			the block offset by the given values. 
		"""
		pass

	@overload
	def toNetherCoords(self) -> "BlockPosHelper":
		"""
		Since: 1.8.4 

		Returns:
			the block position converted to the respective nether coordinates. 
		"""
		pass

	@overload
	def toOverworldCoords(self) -> "BlockPosHelper":
		"""
		Since: 1.8.4 

		Returns:
			the block position converted to the respective overworld coordinates. 
		"""
		pass

	@overload
	def distanceTo(self, entity: EntityHelper) -> float:
		"""
		Since: 1.8.4 

		Args:
			entity: the entity to get the distance to 

		Returns:
			the distance of this position to the given entity. 
		"""
		pass

	@overload
	def distanceTo(self, pos: "BlockPosHelper") -> float:
		"""
		Since: 1.8.4 

		Args:
			pos: the position to get the distance to 

		Returns:
			the distance of this position to the given position. 
		"""
		pass

	@overload
	def distanceTo(self, pos: Pos3D) -> float:
		"""
		Since: 1.8.4 

		Args:
			pos: the position to get the distance to 

		Returns:
			the distance of this position to the given position. 
		"""
		pass

	@overload
	def distanceTo(self, x: float, y: float, z: float) -> float:
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to get the distance to 
			y: the y coordinate to get the distance to 
			z: the z coordinate to get the distance to 

		Returns:
			the distance of this position to the given position. 
		"""
		pass

	@overload
	def toPos3D(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the Pos3D representation of this position. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


