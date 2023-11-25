from typing import overload
from typing import TypeVar
from typing import Mapping

net_minecraft_advancement_AdvancementProgress = TypeVar("net_minecraft_advancement_AdvancementProgress")
AdvancementProgress = net_minecraft_advancement_AdvancementProgress

net_minecraft_advancement_AdvancementEntry = TypeVar("net_minecraft_advancement_AdvancementEntry")
AdvancementEntry = net_minecraft_advancement_AdvancementEntry


class MixinClientAdvancementManager:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getAdvancementProgresses(self) -> Mapping[AdvancementEntry, AdvancementProgress]:
		pass

	pass


