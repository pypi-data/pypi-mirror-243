from typing import overload


class IResourcePackManager:

	@overload
	def jsmacros_disableServerPacks(self, disable: bool) -> None:
		pass

	@overload
	def jsmacros_isServerPacksDisabled(self) -> bool:
		pass

	pass


