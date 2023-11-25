from typing import overload
from typing import TypeVar
from .StateHelper import StateHelper
from .BlockPosHelper import BlockPosHelper
from .Pos3D import Pos3D
from .BlockStateHelper import BlockStateHelper

net_minecraft_fluid_FluidState = TypeVar("net_minecraft_fluid_FluidState")
FluidState = net_minecraft_fluid_FluidState


class FluidStateHelper(StateHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FluidState) -> None:
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the fluid's id. 
		"""
		pass

	@overload
	def isStill(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fluid is still, 'false' otherwise. 
		"""
		pass

	@overload
	def isEmpty(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this fluid is empty (the default fluid state for non fluid blocks), 'false' otherwise. 
		"""
		pass

	@overload
	def getHeight(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the height of this state. 
		"""
		pass

	@overload
	def getLevel(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the level of this state. 
		"""
		pass

	@overload
	def hasRandomTicks(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the fluid has some random tick logic (only used by lava to do the
fire spread), 'false' otherwise. 
		"""
		pass

	@overload
	def getVelocity(self, pos: BlockPosHelper) -> Pos3D:
		"""
		Since: 1.8.4 

		Args:
			pos: the position in the world 

		Returns:
			the velocity that will be applied to entities at the given position. 
		"""
		pass

	@overload
	def getBlockState(self) -> BlockStateHelper:
		"""
		Since: 1.8.4 

		Returns:
			the block state of this fluid. 
		"""
		pass

	@overload
	def getBlastResistance(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the blast resistance of this fluid. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


