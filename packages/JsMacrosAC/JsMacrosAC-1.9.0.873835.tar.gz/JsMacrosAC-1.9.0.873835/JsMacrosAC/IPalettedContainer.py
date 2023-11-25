from typing import overload
from .IPalettedContainerData import IPalettedContainerData


class IPalettedContainer:

	@overload
	def jsmacros_getData(self) -> IPalettedContainerData:
		pass

	pass


