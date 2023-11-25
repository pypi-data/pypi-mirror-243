from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper
from .ItemStackHelper import ItemStackHelper

net_minecraft_entity_decoration_ItemFrameEntity = TypeVar("net_minecraft_entity_decoration_ItemFrameEntity")
ItemFrameEntity = net_minecraft_entity_decoration_ItemFrameEntity


class ItemFrameEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ItemFrameEntity) -> None:
		pass

	@overload
	def isGlowingFrame(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the item frame is glowing, 'false' otherwise. 
		"""
		pass

	@overload
	def getRotation(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the rotation of the item inside this frame. 
		"""
		pass

	@overload
	def getItem(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the item inside this item frame. 
		"""
		pass

	pass


