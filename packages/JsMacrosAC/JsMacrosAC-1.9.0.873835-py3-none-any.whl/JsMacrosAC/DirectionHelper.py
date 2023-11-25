from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .Pos3D import Pos3D

net_minecraft_util_math_Direction = TypeVar("net_minecraft_util_math_Direction")
Direction = net_minecraft_util_math_Direction


class DirectionHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: Direction) -> None:
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this direction. 
		"""
		pass

	@overload
	def getAxis(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of the axis this direction is aligned to. 
		"""
		pass

	@overload
	def isVertical(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this direction is vertical, 'false' otherwise. 
		"""
		pass

	@overload
	def isHorizontal(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this direction is horizontal, 'false' otherwise. 
		"""
		pass

	@overload
	def isTowardsPositive(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this direction is pointing in a positive direction, 'false' otherwise. 
		"""
		pass

	@overload
	def getYaw(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the yaw of this direction. 
		"""
		pass

	@overload
	def getPitch(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the pitch of this direction. 
		"""
		pass

	@overload
	def getOpposite(self) -> "DirectionHelper":
		"""
		Since: 1.8.4 

		Returns:
			the opposite direction. 
		"""
		pass

	@overload
	def getLeft(self) -> "DirectionHelper":
		"""
		Since: 1.8.4 

		Returns:
			the direction to the left. 
		"""
		pass

	@overload
	def getRight(self) -> "DirectionHelper":
		"""
		Since: 1.8.4 

		Returns:
			the direction to the right. 
		"""
		pass

	@overload
	def getVector(self) -> Pos3D:
		"""
		Since: 1.8.4 

		Returns:
			the direction as a directional vector. 
		"""
		pass

	@overload
	def pointsTo(self, yaw: float) -> bool:
		"""
		Since: 1.8.4 

		Args:
			yaw: the yaw to check 

		Returns:
			'true' if the yaw is facing this direction more than any other one, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


