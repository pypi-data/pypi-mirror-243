from typing import overload
from typing import TypeVar
from typing import Generic
from .IllagerEntityHelper import IllagerEntityHelper

T = TypeVar("T")

class SpellcastingIllagerEntityHelper(Generic[T], IllagerEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def isCastingSpell(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this spell caster is currently casting a spell, 'false' otherwise. 
		"""
		pass

	@overload
	def getCastedSpell(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the spell this spell caster is currently casting. 
		"""
		pass

	pass


