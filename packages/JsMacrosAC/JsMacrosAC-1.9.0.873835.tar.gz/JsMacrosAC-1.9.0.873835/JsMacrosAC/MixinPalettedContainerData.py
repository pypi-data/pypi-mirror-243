from typing import overload
from typing import TypeVar
from typing import Generic
from .IPalettedContainerData import IPalettedContainerData

net_minecraft_world_chunk_Palette_T_ = TypeVar("net_minecraft_world_chunk_Palette_T_")
Palette = net_minecraft_world_chunk_Palette_T_

T = TypeVar("T")
net_minecraft_util_collection_PaletteStorage = TypeVar("net_minecraft_util_collection_PaletteStorage")
PaletteStorage = net_minecraft_util_collection_PaletteStorage


class MixinPalettedContainerData(IPalettedContainerData, Generic[T]):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getStorage(self) -> PaletteStorage:
		pass

	@overload
	def jsmacros_getPalette(self) -> Palette:
		pass

	pass


