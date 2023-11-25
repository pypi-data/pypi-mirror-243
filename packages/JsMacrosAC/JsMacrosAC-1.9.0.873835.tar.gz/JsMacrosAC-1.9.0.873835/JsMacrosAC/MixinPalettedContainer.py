from typing import overload
from typing import TypeVar
from typing import Generic
from .IPalettedContainer import IPalettedContainer
from .IPalettedContainerData import IPalettedContainerData

T = TypeVar("T")

class MixinPalettedContainer(IPalettedContainer, Generic[T]):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getData(self) -> IPalettedContainerData:
		pass

	pass


