from typing import overload
from .BlockPosHelper import BlockPosHelper


class InteractionProxy_Break_BreakBlockResult:
	UNAVAILABLE: "InteractionProxy_Break_BreakBlockResult"
	reason: str
	pos: BlockPosHelper

	@overload
	def __init__(self, reason: str, pos: BlockPosHelper) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


