from typing import overload
from typing import TypeVar

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity


class IHorseScreen:

	@overload
	def jsmacros_getEntity(self) -> Entity:
		pass

	pass


