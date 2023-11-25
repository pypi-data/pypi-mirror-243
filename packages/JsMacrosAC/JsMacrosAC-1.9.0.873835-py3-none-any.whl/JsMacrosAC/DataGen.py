from typing import overload
from typing import List


class DataGen:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def main(self, args: List[str]) -> None:
		pass

	pass


