from typing import overload
from typing import TypeVar
from .TraceLine import TraceLine
from .EntityHelper import EntityHelper

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class EntityTraceLine(TraceLine):
	"""
	Since: 1.9.0 
	"""
	dirty: bool
	entity: Entity
	yOffset: float
	shouldRemove: bool

	@overload
	def __init__(self, entity: EntityHelper, color: int, yOffset: float) -> None:
		pass

	@overload
	def __init__(self, entity: EntityHelper, color: int, alpha: int, yOffset: float) -> None:
		pass

	@overload
	def setEntity(self, entity: EntityHelper) -> "EntityTraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def setYOffset(self, yOffset: float) -> "EntityTraceLine":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	pass


