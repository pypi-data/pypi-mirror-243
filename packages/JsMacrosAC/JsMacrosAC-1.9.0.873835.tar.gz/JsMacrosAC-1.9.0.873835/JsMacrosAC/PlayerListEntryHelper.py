from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .TeamHelper import TeamHelper

net_minecraft_client_network_PlayerListEntry = TypeVar("net_minecraft_client_network_PlayerListEntry")
PlayerListEntry = net_minecraft_client_network_PlayerListEntry


class PlayerListEntryHelper(BaseHelper):
	"""
	Since: 1.0.2 
	"""

	@overload
	def __init__(self, p: PlayerListEntry) -> None:
		pass

	@overload
	def getUUID(self) -> str:
		"""
		Since: 1.1.9 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.0.2 
		"""
		pass

	@overload
	def getPing(self) -> int:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getGamemode(self) -> str:
		"""
		Since: 1.6.5 

		Returns:
			null if unknown 
		"""
		pass

	@overload
	def getDisplayText(self) -> TextHelper:
		"""
		Since: 1.1.9 
		"""
		pass

	@overload
	def getPublicKey(self) -> List[float]:
		"""
		Since: 1.8.2 
		"""
		pass

	@overload
	def hasCape(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the player has a cape enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def hasSlimModel(self) -> bool:
		"""A slim skin is an Alex skin, while the default one is Steve.\n
		Since: 1.8.4 

		Returns:
			'true' if the player has a slim skin, 'false' otherwise. 
		"""
		pass

	@overload
	def getSkinTexture(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of the player's skin texture or 'null' if it's unknown. 
		"""
		pass

	@overload
	def getSkinUrl(self) -> str:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def getCapeTexture(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of the player's cape texture or 'null' if it's unknown. 
		"""
		pass

	@overload
	def getElytraTexture(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of the player's elytra texture or 'null' if it's unknown. 
		"""
		pass

	@overload
	def getTeam(self) -> TeamHelper:
		"""
		Since: 1.8.4 

		Returns:
			the team of the player or 'null' if the player is not in a team. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


