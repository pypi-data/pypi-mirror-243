from typing import overload
from typing import List
from typing import Mapping
from .OptionsHelper import OptionsHelper


class OptionsHelper_MusicOptionsHelper:
	parent: OptionsHelper

	@overload
	def __init__(self, OptionsHelper: OptionsHelper) -> None:
		pass

	@overload
	def getParent(self) -> OptionsHelper:
		"""
		Since: 1.8.4 

		Returns:
			the parent options helper. 
		"""
		pass

	@overload
	def getMasterVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current master volume. 
		"""
		pass

	@overload
	def setMasterVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new master volume 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMusicVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current music volume. 
		"""
		pass

	@overload
	def setMusicVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new music volume 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRecordsVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current value of played recods. 
		"""
		pass

	@overload
	def setRecordsVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume for playing records 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getWeatherVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current volume of the weather. 
		"""
		pass

	@overload
	def setWeatherVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume for the weather 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getBlocksVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current volume of block related sounds. 
		"""
		pass

	@overload
	def setBlocksVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume for block sounds 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHostileVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current volume of hostile mobs. 
		"""
		pass

	@overload
	def setHostileVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume for hostile mobs 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getNeutralVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current volume of neutral mobs. 
		"""
		pass

	@overload
	def setNeutralVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume for neutral mobs 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getPlayerVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current player volume. 
		"""
		pass

	@overload
	def setPlayerVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new player volume 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAmbientVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current ambient volume. 
		"""
		pass

	@overload
	def setAmbientVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new ambient volume 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getVoiceVolume(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current voice volume. 
		"""
		pass

	@overload
	def setVoiceVolume(self, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getVolume(self, category: str) -> float:
		"""
		Since: 1.8.4 

		Args:
			category: the category to get the volume of 

		Returns:
			the volume of the given sound category. 
		"""
		pass

	@overload
	def getVolumes(self) -> Mapping[str, Float]:
		"""
		Since: 1.8.4 

		Returns:
			a map of all sound categories and their volumes. 
		"""
		pass

	@overload
	def setVolume(self, category: str, volume: float) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			volume: the new volume 
			category: the category to set the volume for 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSoundDevice(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the currently selected sound device. 
		"""
		pass

	@overload
	def setSoundDevice(self, audioDevice: str) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			audioDevice: the audio device to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAudioDevices(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all connected audio devices. 
		"""
		pass

	@overload
	def areSubtitlesShown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if subtitles should be shown, 'false' otherwise. 
		"""
		pass

	@overload
	def showSubtitles(self, val: bool) -> "OptionsHelper_MusicOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether subtitles should be shown or not 

		Returns:
			self for chaining. 
		"""
		pass

	pass


