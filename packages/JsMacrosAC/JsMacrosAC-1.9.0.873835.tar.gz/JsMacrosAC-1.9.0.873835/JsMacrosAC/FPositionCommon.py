from typing import overload
from .BaseLibrary import BaseLibrary
from .Vec3D import Vec3D
from .EntityHelper import EntityHelper
from .Vec2D import Vec2D
from .Pos3D import Pos3D
from .Pos2D import Pos2D
from .BlockPosHelper import BlockPosHelper


class FPositionCommon(BaseLibrary):
	"""position helper classes\n
	Since: 1.6.3 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def createVec(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> Vec3D:
		"""create a new vector object\n
		Since: 1.6.3 

		Args:
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def createLookingVector(self, entity: EntityHelper) -> Vec3D:
		"""
		Since: 1.8.4 

		Args:
			entity: 
		"""
		pass

	@overload
	def createLookingVector(self, yaw: float, pitch: float) -> Vec3D:
		"""
		Since: 1.8.4 

		Args:
			pitch: 
			yaw: 
		"""
		pass

	@overload
	def createVec(self, x1: float, y1: float, x2: float, y2: float) -> Vec2D:
		"""
		Since: 1.6.3 

		Args:
			y1: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def createPos(self, x: float, y: float, z: float) -> Pos3D:
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def createPos(self, x: float, y: float) -> Pos2D:
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
		"""
		pass

	@overload
	def createBlockPos(self, x: int, y: int, z: int) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Args:
			x: the x position of the block 
			y: the y position of the block 
			z: the z position of the block 

		Returns:
			a BlockPosHelper for the given coordinates. 
		"""
		pass

	pass


