from typing import overload


class MixinStatHandler:

	@overload
	def getStatMap(self) -> Object2IntMap:
		pass

	pass


