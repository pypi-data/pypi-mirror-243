from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .FormattingHelper import FormattingHelper
from .ScoreboardsHelper import ScoreboardsHelper

net_minecraft_scoreboard_Team = TypeVar("net_minecraft_scoreboard_Team")
Team = net_minecraft_scoreboard_Team


class TeamHelper(BaseHelper):
	"""
	Since: 1.3.0 
	"""

	@overload
	def __init__(self, t: Team) -> None:
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getDisplayName(self) -> TextHelper:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getPlayerList(self) -> List[str]:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getColorFormat(self) -> FormattingHelper:
		"""
		Since: 1.8.4 

		Returns:
			the formatting of this team's color. 
		"""
		pass

	@overload
	def getColor(self) -> int:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getColorIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color index of this team. 
		"""
		pass

	@overload
	def getColorValue(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color value for this team or '-1' if it has no color. 
		"""
		pass

	@overload
	def getColorName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the name of this team's color. 
		"""
		pass

	@overload
	def getScoreboard(self) -> ScoreboardsHelper:
		"""
		Since: 1.8.4 

		Returns:
			the scoreboard including this team. 
		"""
		pass

	@overload
	def getPrefix(self) -> TextHelper:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getSuffix(self) -> TextHelper:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getCollisionRule(self) -> str:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def isFriendlyFire(self) -> bool:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def showFriendlyInvisibles(self) -> bool:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def nametagVisibility(self) -> str:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def deathMessageVisibility(self) -> str:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


