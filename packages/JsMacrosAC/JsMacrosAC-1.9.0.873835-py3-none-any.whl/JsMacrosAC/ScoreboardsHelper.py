from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .ScoreboardObjectiveHelper import ScoreboardObjectiveHelper
from .PlayerEntityHelper import PlayerEntityHelper
from .FormattingHelper import FormattingHelper
from .TeamHelper import TeamHelper

net_minecraft_scoreboard_Scoreboard = TypeVar("net_minecraft_scoreboard_Scoreboard")
Scoreboard = net_minecraft_scoreboard_Scoreboard


class ScoreboardsHelper(BaseHelper):
	"""
	Since: 1.2.9 
	"""

	@overload
	def __init__(self, board: Scoreboard) -> None:
		pass

	@overload
	def getObjectiveForTeamColorIndex(self, index: int) -> ScoreboardObjectiveHelper:
		"""
		Since: 1.2.9 

		Args:
			index: 
		"""
		pass

	@overload
	def getObjectiveSlot(self, slot: int) -> ScoreboardObjectiveHelper:
		"""'0' is tab list, '1' or '3 + getPlayerTeamColorIndex()' is sidebar, '2' should be below name.
therefore max slot number is 18.\n
		Since: 1.2.9 

		Args:
			slot: 
		"""
		pass

	@overload
	def getPlayerTeamColorIndex(self, entity: PlayerEntityHelper) -> int:
		"""
		Since: 1.2.9 

		Args:
			entity: 
		"""
		pass

	@overload
	def getPlayerTeamColorIndex(self) -> int:
		"""
		Since: 1.6.5 

		Returns:
			team index for client player 
		"""
		pass

	@overload
	def getTeamColorFormatting(self) -> FormattingHelper:
		"""
		Since: 1.8.4 

		Returns:
			the formatting for the client player's team, 'null' if the player is not in a
team. 
		"""
		pass

	@overload
	def getTeamColorFormatting(self, player: PlayerEntityHelper) -> FormattingHelper:
		"""
		Since: 1.8.4 

		Args:
			player: the player to get the team color's formatting for. 

		Returns:
			the formatting for the client player's team, 'null' if the player is not in a
team. 
		"""
		pass

	@overload
	def getTeamColor(self, player: PlayerEntityHelper) -> int:
		"""
		Since: 1.8.4 

		Args:
			player: the player to get the team color for 

		Returns:
			the color of the specified player's team or '-1' if the player is not in a team. 
		"""
		pass

	@overload
	def getTeamColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the color of this player's team or '-1' if this player is not in a team. 
		"""
		pass

	@overload
	def getTeamColorName(self, player: PlayerEntityHelper) -> str:
		"""
		Since: 1.8.4 

		Args:
			player: the player to get the team color's name for 

		Returns:
			the name of the specified player's team color or 'null' if the player is not in
a team. 
		"""
		pass

	@overload
	def getTeamColorName(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the color of this player's team or 'null' if this player is not in a team. 
		"""
		pass

	@overload
	def getTeams(self) -> List[TeamHelper]:
		"""
		Since: 1.3.0 
		"""
		pass

	@overload
	def getPlayerTeam(self, p: PlayerEntityHelper) -> TeamHelper:
		"""
		Since: 1.3.0 

		Args:
			p: 
		"""
		pass

	@overload
	def getPlayerTeam(self) -> TeamHelper:
		"""
		Since: 1.6.5 

		Returns:
			team for client player 
		"""
		pass

	@overload
	def getCurrentScoreboard(self) -> ScoreboardObjectiveHelper:
		"""
		Since: 1.2.9 

		Returns:
			the ScoreboardObjectiveHelper for the currently displayed sidebar scoreboard. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


