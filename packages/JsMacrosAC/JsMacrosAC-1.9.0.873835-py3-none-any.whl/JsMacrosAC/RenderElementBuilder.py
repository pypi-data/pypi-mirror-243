from typing import overload
from typing import TypeVar
from typing import Generic

T = TypeVar("T")

class RenderElementBuilder(Generic[T]):
	"""
	Since: 1.8.4 
	"""

	@overload
	def build(self) -> T:
		"""
		Since: 1.8.4 

		Returns:
			the newly created element. 
		"""
		pass

	@overload
	def buildAndAdd(self) -> T:
		"""Builds and adds the element to the draw2D the builder was created from.\n
		Since: 1.8.4 

		Returns:
			the newly created element. 
		"""
		pass

	pass


