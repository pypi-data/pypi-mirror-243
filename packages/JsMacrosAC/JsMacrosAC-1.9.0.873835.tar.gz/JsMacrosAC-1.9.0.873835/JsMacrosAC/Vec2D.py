from typing import overload
from .Pos2D import Pos2D
from .Vec3D import Vec3D


class Vec2D:
	"""
	Since: 1.2.6 [citation needed] 
	"""
	x1: float
	y1: float
	x2: float
	y2: float

	@overload
	def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
		pass

	@overload
	def __init__(self, start: Pos2D, end: Pos2D) -> None:
		pass

	@overload
	def getX1(self) -> float:
		pass

	@overload
	def getY1(self) -> float:
		pass

	@overload
	def getX2(self) -> float:
		pass

	@overload
	def getY2(self) -> float:
		pass

	@overload
	def getDeltaX(self) -> float:
		pass

	@overload
	def getDeltaY(self) -> float:
		pass

	@overload
	def getStart(self) -> Pos2D:
		pass

	@overload
	def getEnd(self) -> Pos2D:
		pass

	@overload
	def getMagnitude(self) -> float:
		pass

	@overload
	def getMagnitudeSq(self) -> float:
		"""
		Since: 1.6.5 

		Returns:
			magnitude squared 
		"""
		pass

	@overload
	def add(self, vec: "Vec2D") -> "Vec2D":
		pass

	@overload
	def add(self, x1: float, y1: float, x2: float, y2: float) -> "Vec2D":
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
	def multiply(self, vec: "Vec2D") -> "Vec2D":
		pass

	@overload
	def multiply(self, x1: float, y1: float, x2: float, y2: float) -> "Vec2D":
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
	def scale(self, scale: float) -> "Vec2D":
		"""
		Since: 1.6.3 

		Args:
			scale: 
		"""
		pass

	@overload
	def dotProduct(self, vec: "Vec2D") -> float:
		pass

	@overload
	def reverse(self) -> "Vec2D":
		pass

	@overload
	def normalize(self) -> "Vec2D":
		"""
		Since: 1.6.5 

		Returns:
			a new Vec2D with the same direction but a magnitude of 1 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def to3D(self) -> Vec3D:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareTo(self, other: "Vec2D") -> int:
		pass

	pass


