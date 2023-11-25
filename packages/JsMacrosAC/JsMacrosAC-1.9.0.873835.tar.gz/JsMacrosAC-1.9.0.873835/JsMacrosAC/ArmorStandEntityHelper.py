from typing import overload
from typing import List
from typing import TypeVar
from .LivingEntityHelper import LivingEntityHelper

net_minecraft_entity_decoration_ArmorStandEntity = TypeVar("net_minecraft_entity_decoration_ArmorStandEntity")
ArmorStandEntity = net_minecraft_entity_decoration_ArmorStandEntity


class ArmorStandEntityHelper(LivingEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ArmorStandEntity) -> None:
		pass

	@overload
	def isVisible(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the armor stand is visible, 'false' otherwise. 
		"""
		pass

	@overload
	def isSmall(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the armor is small, 'false' otherwise. 
		"""
		pass

	@overload
	def hasArms(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the armor stand has arms, 'false' otherwise. 
		"""
		pass

	@overload
	def hasBasePlate(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the armor stand has a base plate, 'false' otherwise. 
		"""
		pass

	@overload
	def isMarker(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the armor stand is a marker, 'false' otherwise. 
		"""
		pass

	@overload
	def getHeadRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the head rotation of the armor stand. 
		"""
		pass

	@overload
	def getBodyRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the body rotation of the armor stand. 
		"""
		pass

	@overload
	def getLeftArmRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the left arm rotation of the armor stand. 
		"""
		pass

	@overload
	def getRightArmRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the right arm rotation of the armor stand. 
		"""
		pass

	@overload
	def getLeftLegRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the left leg rotation of the armor stand. 
		"""
		pass

	@overload
	def getRightLegRotation(self) -> List[float]:
		"""The rotation is in the format of '[yaw, pitch, roll]' .\n
		Since: 1.8.4 

		Returns:
			the right leg rotation of the armor stand. 
		"""
		pass

	pass


