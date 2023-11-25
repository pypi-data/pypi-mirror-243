from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .EntityHelper import EntityHelper

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity


class EventRiding(BaseEvent):
	"""
	Since: 1.5.0 
	"""
	state: bool
	entity: EntityHelper

	@overload
	def __init__(self, state: bool, entity: Entity) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


