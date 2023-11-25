from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .EntityHelper import EntityHelper

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

net_minecraft_entity_Entity_RemovalReason = TypeVar("net_minecraft_entity_Entity_RemovalReason")
Entity_RemovalReason = net_minecraft_entity_Entity_RemovalReason


class EventEntityUnload(BaseEvent):
	entity: EntityHelper
	reason: str

	@overload
	def __init__(self, e: Entity, reason: Entity_RemovalReason) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


