from typing import overload
from typing import TypeVar
from typing import Generic
from .LivingEntityHelper import LivingEntityHelper

T = TypeVar("T")

class MobEntityHelper(Generic[T], LivingEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isAttacking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the entity is currently attacking something, 'false' otherwise. 
		"""
		pass

	@overload
	def isAiDisabled(self) -> bool:
		"""Mobs which have there AI disabled don't move, attack, or interact with the world by
themselves.\n
		Since: 1.8.4 

		Returns:
			'true' if the entity's AI is disabled, 'false' otherwise. 
		"""
		pass

	pass


