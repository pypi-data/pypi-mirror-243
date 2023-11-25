from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper

net_minecraft_client_network_ServerInfo = TypeVar("net_minecraft_client_network_ServerInfo")
ServerInfo = net_minecraft_client_network_ServerInfo


class ServerInfoHelper(BaseHelper):
	"""
	Since: 1.6.5 
	"""

	@overload
	def __init__(self, base: ServerInfo) -> None:
		pass

	@overload
	def getName(self) -> str:
		pass

	@overload
	def getAddress(self) -> str:
		pass

	@overload
	def getPlayerCountLabel(self) -> TextHelper:
		pass

	@overload
	def getLabel(self) -> TextHelper:
		pass

	@overload
	def getPing(self) -> float:
		pass

	@overload
	def getProtocolVersion(self) -> int:
		pass

	@overload
	def getVersion(self) -> TextHelper:
		pass

	@overload
	def getPlayerListSummary(self) -> List[TextHelper]:
		pass

	@overload
	def resourcePackPolicy(self) -> str:
		pass

	@overload
	def getIcon(self) -> List[float]:
		pass

	@overload
	def isOnline(self) -> bool:
		pass

	@overload
	def isLocal(self) -> bool:
		pass

	@overload
	def getNbt(self) -> NBTElementHelper_NBTCompoundHelper:
		pass

	@overload
	def isSecureChatEnforced(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the server enforces secure chat, 'false' otherwise. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


