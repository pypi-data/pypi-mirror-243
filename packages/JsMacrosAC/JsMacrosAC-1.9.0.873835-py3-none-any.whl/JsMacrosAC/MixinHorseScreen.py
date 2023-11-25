from typing import overload
from typing import TypeVar
from .IHorseScreen import IHorseScreen

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity


class MixinHorseScreen(IHorseScreen):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getEntity(self) -> Entity:
		pass

	pass


