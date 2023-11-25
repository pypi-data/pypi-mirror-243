from typing import overload
from typing import TypeVar
from typing import Set

net_minecraft_util_Identifier = TypeVar("net_minecraft_util_Identifier")
Identifier = net_minecraft_util_Identifier


class IFontManager:

	@overload
	def jsmacros_getFontList(self) -> Set[Identifier]:
		pass

	pass


