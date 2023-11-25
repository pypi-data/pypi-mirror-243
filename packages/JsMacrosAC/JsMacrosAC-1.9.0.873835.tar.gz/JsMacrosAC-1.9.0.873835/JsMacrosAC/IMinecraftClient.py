from typing import overload
from typing import TypeVar

net_minecraft_client_font_FontManager = TypeVar("net_minecraft_client_font_FontManager")
FontManager = net_minecraft_client_font_FontManager


class IMinecraftClient:

	@overload
	def jsmacros_getFontManager(self) -> FontManager:
		pass

	@overload
	def jsmacros_doItemUse(self) -> None:
		pass

	@overload
	def jsmacros_doAttack(self) -> None:
		pass

	pass


