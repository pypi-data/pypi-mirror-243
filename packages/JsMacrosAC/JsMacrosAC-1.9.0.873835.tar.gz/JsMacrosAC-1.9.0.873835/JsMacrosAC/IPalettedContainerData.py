from typing import overload
from typing import TypeVar

net_minecraft_world_chunk_Palette_T_ = TypeVar("net_minecraft_world_chunk_Palette_T_")
Palette = net_minecraft_world_chunk_Palette_T_

net_minecraft_util_collection_PaletteStorage = TypeVar("net_minecraft_util_collection_PaletteStorage")
PaletteStorage = net_minecraft_util_collection_PaletteStorage


class IPalettedContainerData:

	@overload
	def jsmacros_getStorage(self) -> PaletteStorage:
		pass

	@overload
	def jsmacros_getPalette(self) -> Palette:
		pass

	pass


