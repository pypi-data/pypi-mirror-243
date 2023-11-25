from typing import overload
from typing import TypeVar

net_minecraft_entity_data_TrackedData_java_lang_Byte_ = TypeVar("net_minecraft_entity_data_TrackedData_java_lang_Byte_")
TrackedData = net_minecraft_entity_data_TrackedData_java_lang_Byte_


class MixinTridentEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getLoyalty(self) -> TrackedData:
		pass

	pass


