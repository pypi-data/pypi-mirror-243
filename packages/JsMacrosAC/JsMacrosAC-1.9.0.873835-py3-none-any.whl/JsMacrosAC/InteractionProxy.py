from typing import overload


class InteractionProxy:
	"""A class that can override crosshair target, handle breaking block and long interact.\n
	Since: 1.9.0 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def reset(self) -> None:
		pass

	pass


