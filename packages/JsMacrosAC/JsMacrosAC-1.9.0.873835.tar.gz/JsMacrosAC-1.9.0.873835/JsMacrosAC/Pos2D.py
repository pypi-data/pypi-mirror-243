from typing import overload
from .Pos3D import Pos3D
from .Vec2D import Vec2D


class Pos2D:
	"""
	Since: 1.2.6 [citation needed] 
	"""
	ZERO: "Pos2D"
	x: float
	y: float

	@overload
	def __init__(self, x: float, y: float) -> None:
		pass

	@overload
	def getX(self) -> float:
		pass

	@overload
	def getY(self) -> float:
		pass

	@overload
	def add(self, pos: "Pos2D") -> "Pos2D":
		pass

	@overload
	def add(self, x: float, y: float) -> "Pos2D":
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
		"""
		pass

	@overload
	def sub(self, pos: "Pos2D") -> "Pos2D":
		"""
		Since: 1.8.4 

		Args:
			pos: the position to subtract 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def sub(self, x: float, y: float) -> "Pos2D":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to subtract 
			y: the y coordinate to subtract 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def multiply(self, pos: "Pos2D") -> "Pos2D":
		pass

	@overload
	def multiply(self, x: float, y: float) -> "Pos2D":
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
		"""
		pass

	@overload
	def divide(self, pos: "Pos2D") -> "Pos2D":
		"""
		Since: 1.8.4 

		Args:
			pos: the position to divide by 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def divide(self, x: float, y: float) -> "Pos2D":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to divide by 
			y: the y coordinate to divide by 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def scale(self, scale: float) -> "Pos2D":
		"""
		Since: 1.6.3 

		Args:
			scale: 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def to3D(self) -> Pos3D:
		pass

	@overload
	def toVector(self) -> Vec2D:
		pass

	@overload
	def toVector(self, start_pos: "Pos2D") -> Vec2D:
		"""
		Since: 1.6.4 

		Args:
			start_pos: 
		"""
		pass

	@overload
	def toVector(self, start_x: float, start_y: float) -> Vec2D:
		"""
		Since: 1.6.4 

		Args:
			start_x: 
			start_y: 
		"""
		pass

	@overload
	def toReverseVector(self) -> Vec2D:
		"""
		Since: 1.6.4 
		"""
		pass

	@overload
	def toReverseVector(self, end_pos: "Pos2D") -> Vec2D:
		"""
		Since: 1.6.4 

		Args:
			end_pos: 
		"""
		pass

	@overload
	def toReverseVector(self, end_x: float, end_y: float) -> Vec2D:
		"""
		Since: 1.6.4 

		Args:
			end_x: 
			end_y: 
		"""
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareTo(self, o: "Pos2D") -> int:
		pass

	pass


