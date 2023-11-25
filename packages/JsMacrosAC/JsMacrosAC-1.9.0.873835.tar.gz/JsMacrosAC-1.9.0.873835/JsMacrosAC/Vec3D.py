from typing import overload
from typing import TypeVar
from .Vec2D import Vec2D
from .Pos3D import Pos3D

org_joml_Vector3f = TypeVar("org_joml_Vector3f")
Vector3f = org_joml_Vector3f


class Vec3D(Vec2D):
	"""
	Since: 1.2.6 [citation needed] 
	"""
	z1: float
	z2: float

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
		pass

	@overload
	def __init__(self, start: Pos3D, end: Pos3D) -> None:
		pass

	@overload
	def getZ1(self) -> float:
		pass

	@overload
	def getZ2(self) -> float:
		pass

	@overload
	def getDeltaZ(self) -> float:
		pass

	@overload
	def getStart(self) -> Pos3D:
		pass

	@overload
	def getEnd(self) -> Pos3D:
		pass

	@overload
	def getMagnitude(self) -> float:
		pass

	@overload
	def getMagnitudeSq(self) -> float:
		pass

	@overload
	def add(self, vec: "Vec3D") -> "Vec3D":
		pass

	@overload
	def addStart(self, pos: Pos3D) -> "Vec3D":
		"""
		Since: 1.6.4 

		Args:
			pos: 
		"""
		pass

	@overload
	def addEnd(self, pos: Pos3D) -> "Vec3D":
		"""
		Since: 1.6.4 

		Args:
			pos: 
		"""
		pass

	@overload
	def addStart(self, x: float, y: float, z: float) -> "Vec3D":
		"""
		Since: 1.6.4 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def addEnd(self, x: float, y: float, z: float) -> "Vec3D":
		"""
		Since: 1.6.4 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def add(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> "Vec3D":
		"""
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
	def multiply(self, vec: "Vec3D") -> "Vec3D":
		pass

	@overload
	def multiply(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> "Vec3D":
		"""
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
	def scale(self, scale: float) -> "Vec3D":
		"""
		Since: 1.6.3 

		Args:
			scale: 
		"""
		pass

	@overload
	def normalize(self) -> "Vec3D":
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getPitch(self) -> float:
		pass

	@overload
	def getYaw(self) -> float:
		pass

	@overload
	def dotProduct(self, vec: "Vec3D") -> float:
		pass

	@overload
	def crossProduct(self, vec: "Vec3D") -> "Vec3D":
		pass

	@overload
	def reverse(self) -> "Vec3D":
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def toMojangFloatVector(self) -> Vector3f:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	@overload
	def compareTo(self, o: "Vec3D") -> int:
		pass

	pass


