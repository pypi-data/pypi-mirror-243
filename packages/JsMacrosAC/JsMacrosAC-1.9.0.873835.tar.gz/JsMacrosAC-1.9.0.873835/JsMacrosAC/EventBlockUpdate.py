from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .BlockDataHelper import BlockDataHelper

net_minecraft_block_BlockState = TypeVar("net_minecraft_block_BlockState")
BlockState = net_minecraft_block_BlockState

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos

net_minecraft_block_entity_BlockEntity = TypeVar("net_minecraft_block_entity_BlockEntity")
BlockEntity = net_minecraft_block_entity_BlockEntity


class EventBlockUpdate(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	block: BlockDataHelper
	updateType: str

	@overload
	def __init__(self, block: BlockState, blockEntity: BlockEntity, blockPos: BlockPos, updateType: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


