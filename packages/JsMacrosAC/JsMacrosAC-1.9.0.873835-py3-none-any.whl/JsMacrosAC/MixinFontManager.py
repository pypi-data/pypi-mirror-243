from typing import overload
from typing import TypeVar
from typing import Set
from .IFontManager import IFontManager

net_minecraft_util_Identifier = TypeVar("net_minecraft_util_Identifier")
Identifier = net_minecraft_util_Identifier


class MixinFontManager(IFontManager):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getFontList(self) -> Set[Identifier]:
		pass

	pass


