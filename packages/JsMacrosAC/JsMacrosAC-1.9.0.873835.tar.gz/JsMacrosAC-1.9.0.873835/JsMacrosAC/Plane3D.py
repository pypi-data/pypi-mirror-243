from typing import overload
from .Vec3D import Vec3D


class Plane3D:
	"""
	Since: 1.6.5 
	"""
	x1: float
	y1: float
	z1: float
	x2: float
	y2: float
	z2: float
	x3: float
	y3: float
	z3: float

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, x3: float, y3: float, z3: float) -> None:
		pass

	@overload
	def getNormalVector(self) -> Vec3D:
		pass

	@overload
	def getVec12(self) -> Vec3D:
		pass

	@overload
	def getVec13(self) -> Vec3D:
		pass

	@overload
	def getVec23(self) -> Vec3D:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def hashCode(self) -> int:
		pass

	pass


