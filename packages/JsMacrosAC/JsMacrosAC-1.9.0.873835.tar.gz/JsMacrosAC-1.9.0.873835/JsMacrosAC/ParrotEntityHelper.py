from typing import overload
from typing import TypeVar
from .TameableEntityHelper import TameableEntityHelper

net_minecraft_entity_passive_ParrotEntity = TypeVar("net_minecraft_entity_passive_ParrotEntity")
ParrotEntity = net_minecraft_entity_passive_ParrotEntity


class ParrotEntityHelper(TameableEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ParrotEntity) -> None:
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this parrot. 
		"""
		pass

	@overload
	def isSitting(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this parrot is sitting, 'false' otherwise. 
		"""
		pass

	@overload
	def isFlying(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this parrot is flying, 'false' otherwise. 
		"""
		pass

	@overload
	def isPartying(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this parrot is dancing to music, 'false' otherwise. 
		"""
		pass

	@overload
	def isStanding(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this parrot is just standing around, 'false' otherwise. 
		"""
		pass

	@overload
	def isSittingOnShoulder(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this parrot is sitting on any player's shoulder, 'false' otherwise. 
		"""
		pass

	pass


