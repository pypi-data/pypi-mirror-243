from typing import overload
from typing import TypeVar
from typing import Generic
from .DonkeyEntityHelper import DonkeyEntityHelper
from .DyeColorHelper import DyeColorHelper

T = TypeVar("T")

class LlamaEntityHelper(Generic[T], DonkeyEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this llama. 
		"""
		pass

	@overload
	def getCarpetColor(self) -> DyeColorHelper:
		"""
		Since: 1.8.4 

		Returns:
			the color of this llama's carpet. 
		"""
		pass

	@overload
	def getStrength(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the strength of this llama. 
		"""
		pass

	@overload
	def isTraderLlama(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this llama belongs to a wandering trader, 'false' otherwise. 
		"""
		pass

	pass


