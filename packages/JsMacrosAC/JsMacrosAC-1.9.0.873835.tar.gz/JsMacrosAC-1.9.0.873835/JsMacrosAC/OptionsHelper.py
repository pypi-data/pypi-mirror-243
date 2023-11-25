from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .OptionsHelper_SkinOptionsHelper import OptionsHelper_SkinOptionsHelper
from .OptionsHelper_VideoOptionsHelper import OptionsHelper_VideoOptionsHelper
from .OptionsHelper_MusicOptionsHelper import OptionsHelper_MusicOptionsHelper
from .OptionsHelper_ControlOptionsHelper import OptionsHelper_ControlOptionsHelper
from .OptionsHelper_ChatOptionsHelper import OptionsHelper_ChatOptionsHelper
from .OptionsHelper_AccessibilityOptionsHelper import OptionsHelper_AccessibilityOptionsHelper

net_minecraft_client_option_GameOptions = TypeVar("net_minecraft_client_option_GameOptions")
GameOptions = net_minecraft_client_option_GameOptions


class OptionsHelper(BaseHelper):
	"""
	Since: 1.8.4 
	"""
	skin: OptionsHelper_SkinOptionsHelper
	video: OptionsHelper_VideoOptionsHelper
	music: OptionsHelper_MusicOptionsHelper
	control: OptionsHelper_ControlOptionsHelper
	chat: OptionsHelper_ChatOptionsHelper
	accessibility: OptionsHelper_AccessibilityOptionsHelper

	@overload
	def __init__(self, options: GameOptions) -> None:
		pass

	@overload
	def getSkinOptions(self) -> OptionsHelper_SkinOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the skin options. 
		"""
		pass

	@overload
	def getVideoOptions(self) -> OptionsHelper_VideoOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the video options. 
		"""
		pass

	@overload
	def getMusicOptions(self) -> OptionsHelper_MusicOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the music options. 
		"""
		pass

	@overload
	def getControlOptions(self) -> OptionsHelper_ControlOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the control options. 
		"""
		pass

	@overload
	def getChatOptions(self) -> OptionsHelper_ChatOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the chat options. 
		"""
		pass

	@overload
	def getAccessibilityOptions(self) -> OptionsHelper_AccessibilityOptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			a helper for the accessibility options. 
		"""
		pass

	@overload
	def saveOptions(self) -> "OptionsHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getResourcePacks(self) -> List[str]:
		"""
		Since: 1.1.7 

		Returns:
			list of names of resource packs. 
		"""
		pass

	@overload
	def getEnabledResourcePacks(self) -> List[str]:
		"""
		Since: 1.2.0 

		Returns:
			list of names of enabled resource packs. 
		"""
		pass

	@overload
	def setEnabledResourcePacks(self, enabled: List[str]) -> "OptionsHelper":
		"""Set the enabled resource packs to the provided list.\n
		Since: 1.2.0 

		Args:
			enabled: 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def removeServerResourcePack(self, state: bool) -> "OptionsHelper":
		"""
		Since: 1.8.3 

		Args:
			state: false to put it back 
		"""
		pass

	@overload
	def getLanguage(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the active language. 
		"""
		pass

	@overload
	def setLanguage(self, languageCode: str) -> "OptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			languageCode: the language to change to 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getDifficulty(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the active difficulty. 
		"""
		pass

	@overload
	def setDifficulty(self, name: str) -> "OptionsHelper":
		"""The name be either "peaceful", "easy", "normal", or "hard".\n
		Since: 1.8.4 

		Args:
			name: the name of the difficulty to change to 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isDifficultyLocked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the difficulty is locked, 'false' otherwise. 
		"""
		pass

	@overload
	def lockDifficulty(self) -> "OptionsHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def unlockDifficulty(self) -> "OptionsHelper":
		"""Unlocks the difficulty of the world. This can't be done in an unmodified client.\n
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getFov(self) -> int:
		"""
		Since: 1.1.7 

		Returns:
			the current fov value. 
		"""
		pass

	@overload
	def setFov(self, fov: int) -> "OptionsHelper":
		"""
		Since: 1.1.7 

		Args:
			fov: the new fov value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getCameraMode(self) -> int:
		"""
		Since: 1.5.0 

		Returns:
			0 for 1st person, 2 for in front. 
		"""
		pass

	@overload
	def setCameraMode(self, mode: int) -> "OptionsHelper":
		"""
		Since: 1.5.0 

		Args:
			mode: 0: first, 2: front 
		"""
		pass

	@overload
	def getSmoothCamera(self) -> bool:
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def setSmoothCamera(self, val: bool) -> "OptionsHelper":
		"""
		Since: 1.5.0 

		Args:
			val: 
		"""
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.2.6 
		"""
		pass

	@overload
	def setWidth(self, w: int) -> "OptionsHelper":
		"""
		Since: 1.2.6 

		Args:
			w: 
		"""
		pass

	@overload
	def setHeight(self, h: int) -> "OptionsHelper":
		"""
		Since: 1.2.6 

		Args:
			h: 
		"""
		pass

	@overload
	def setSize(self, w: int, h: int) -> "OptionsHelper":
		"""
		Since: 1.2.6 

		Args:
			w: 
			h: 
		"""
		pass

	@overload
	def getCloudMode(self) -> int:
		"""
		Since: 1.1.7 

		Returns:
			0: off, 2: fancy 
		"""
		pass

	@overload
	def setCloudMode(self, mode: int) -> "OptionsHelper":
		"""
		Since: 1.1.7 

		Args:
			mode: 0: off, 2: fancy 
		"""
		pass

	@overload
	def getGraphicsMode(self) -> int:
		"""
		Since: 1.1.7 
		"""
		pass

	@overload
	def setGraphicsMode(self, mode: int) -> "OptionsHelper":
		"""
		Since: 1.1.7 

		Args:
			mode: 0: fast, 2: fabulous 
		"""
		pass

	@overload
	def isRightHanded(self) -> bool:
		"""
		Since: 1.1.7 
		"""
		pass

	@overload
	def setRightHanded(self, val: bool) -> "OptionsHelper":
		"""
		Since: 1.1.7 

		Args:
			val: 
		"""
		pass

	@overload
	def getRenderDistance(self) -> int:
		"""
		Since: 1.1.7 
		"""
		pass

	@overload
	def setRenderDistance(self, d: int) -> "OptionsHelper":
		"""
		Since: 1.1.7 

		Args:
			d: 
		"""
		pass

	@overload
	def getGamma(self) -> float:
		"""
		Since: 1.3.0 normal values for gamma are between '0' and '1' 
		"""
		pass

	@overload
	def setGamma(self, gamma: float) -> "OptionsHelper":
		"""
		Since: 1.3.0 normal values for gamma are between '0' and '1' 
		"""
		pass

	@overload
	def setVolume(self, vol: float) -> "OptionsHelper":
		"""
		Since: 1.3.1 

		Args:
			vol: 
		"""
		pass

	@overload
	def setVolume(self, category: str, volume: float) -> "OptionsHelper":
		"""set volume by category.\n
		Since: 1.3.1 

		Args:
			volume: 
			category: 
		"""
		pass

	@overload
	def getVolumes(self) -> Mapping[str, Float]:
		"""
		Since: 1.3.1 
		"""
		pass

	@overload
	def setGuiScale(self, scale: int) -> "OptionsHelper":
		"""sets gui scale, '0' for auto.\n
		Since: 1.3.1 

		Args:
			scale: 
		"""
		pass

	@overload
	def getGuiScale(self) -> int:
		"""
		Since: 1.3.1 

		Returns:
			gui scale, '0' for auto. 
		"""
		pass

	@overload
	def getVolume(self, category: str) -> float:
		"""
		Since: 1.3.1 

		Args:
			category: 
		"""
		pass

	pass


