from typing import overload
from typing import TypeVar
from .StateHelper import StateHelper
from .BlockHelper import BlockHelper
from .FluidStateHelper import FluidStateHelper
from .BlockPosHelper import BlockPosHelper
from .UniversalBlockStateHelper import UniversalBlockStateHelper

net_minecraft_block_BlockState = TypeVar("net_minecraft_block_BlockState")
BlockState = net_minecraft_block_BlockState


class BlockStateHelper(StateHelper):
	"""
	Since: 1.6.5 
	"""

	@overload
	def __init__(self, base: BlockState) -> None:
		pass

	@overload
	def getBlock(self) -> BlockHelper:
		"""
		Since: 1.6.5 

		Returns:
			the block the state belongs to. 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the block's id. 
		"""
		pass

	@overload
	def getFluidState(self) -> FluidStateHelper:
		"""
		Since: 1.8.4 

		Returns:
			the fluid state of this block state. 
		"""
		pass

	@overload
	def getHardness(self) -> float:
		"""
		Since: 1.6.5 

		Returns:
			the hardness. 
		"""
		pass

	@overload
	def getLuminance(self) -> int:
		"""
		Since: 1.6.5 

		Returns:
			the luminance. 
		"""
		pass

	@overload
	def emitsRedstonePower(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state emits redstone power. 
		"""
		pass

	@overload
	def exceedsCube(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the shape of the state is a cube. 
		"""
		pass

	@overload
	def isAir(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state is air. 
		"""
		pass

	@overload
	def isOpaque(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state is opaque. 
		"""
		pass

	@overload
	def isToolRequired(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if a tool is required to mine the block. 
		"""
		pass

	@overload
	def hasBlockEntity(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state has a block entity. 
		"""
		pass

	@overload
	def hasRandomTicks(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state can be random ticked. 
		"""
		pass

	@overload
	def hasComparatorOutput(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state has a comparator output. 
		"""
		pass

	@overload
	def getPistonBehaviour(self) -> str:
		"""
		Since: 1.6.5 

		Returns:
			the piston behaviour of the state. 
		"""
		pass

	@overload
	def blocksMovement(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state blocks the movement of entities. 
		"""
		pass

	@overload
	def isBurnable(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state is burnable. 
		"""
		pass

	@overload
	def isLiquid(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state is a liquid. 
		"""
		pass

	@overload
	def isSolid(self) -> bool:
		"""
		Since: 1.6.5 

		Returns:
			'true' if the state is solid. 
		"""
		pass

	@overload
	def isReplaceable(self) -> bool:
		"""This will return true for blocks like air and grass, that can be replaced without breaking
them first.\n
		Since: 1.6.5 

		Returns:
			'true' if the state can be replaced. 
		"""
		pass

	@overload
	def allowsSpawning(self, pos: BlockPosHelper, entity: str) -> bool:
		"""
		Since: 1.6.5 

		Args:
			pos: the position of the block to check 
			entity: the entity type to check 

		Returns:
			'true' if the entity can spawn on this block state at the given position in the
current world. 
		"""
		pass

	@overload
	def shouldSuffocate(self, pos: BlockPosHelper) -> bool:
		"""
		Since: 1.6.5 

		Args:
			pos: the position of the block to check 

		Returns:
			'true' if an entity can suffocate in this block state at the given position in
the current world. 
		"""
		pass

	@overload
	def getUniversal(self) -> UniversalBlockStateHelper:
		"""
		Since: 1.8.4 

		Returns:
			an UniversalBlockStateHelper to access all properties of this block state. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


