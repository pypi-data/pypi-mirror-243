from typing import overload
from .OptionsHelper import OptionsHelper


class OptionsHelper_VideoOptionsHelper:
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
	def getFullscreenResolution(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the full screen resolution as a string. 
		"""
		pass

	@overload
	def getBiomeBlendRadius(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current biome blend radius. 
		"""
		pass

	@overload
	def setBiomeBlendRadius(self, radius: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			radius: the new biome blend radius 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getGraphicsMode(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the selected graphics mode. 
		"""
		pass

	@overload
	def setGraphicsMode(self, mode: str) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the graphics mode to select. Must be either "fast", "fancy" or "fabulous" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getChunkBuilderMode(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the selected chunk builder mode. 
		"""
		pass

	@overload
	def setChunkBuilderMode(self, mode: str) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the chunk builder mode to select. Must be either "none", "nearby" or
            "player_affected" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSmoothLightningMode(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			the selected smooth lightning mode. 
		"""
		pass

	@overload
	def setSmoothLightningMode(self, mode: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the smooth lightning mode to select. boolean value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getRenderDistance(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current render distance in chunks. 
		"""
		pass

	@overload
	def setRenderDistance(self, radius: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			radius: the new render distance in chunks 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getSimulationDistance(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current simulation distance in chunks. 
		"""
		pass

	@overload
	def setSimulationDistance(self, radius: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			radius: the new simulation distance in chunks 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMaxFps(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current upper fps limit. 
		"""
		pass

	@overload
	def setMaxFps(self, maxFps: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			maxFps: the new maximum fps limit 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isVsyncEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if vsync is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableVsync(self, val: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable vsync or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isViewBobbingEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if view bobbing is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableViewBobbing(self, val: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable view bobbing or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getGuiScale(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current gui scale. 
		"""
		pass

	@overload
	def setGuiScale(self, scale: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			scale: the gui scale to set. Must be 1, 2, 3 or 4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAttackIndicatorType(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current attack indicator type. 
		"""
		pass

	@overload
	def setAttackIndicatorType(self, type: str) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			type: the attack indicator type. Must be either "off", "crosshair", or "hotbar" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getGamma(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current gamma value. 
		"""
		pass

	@overload
	def setGamma(self, gamma: float) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			gamma: the new gamma value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getBrightness(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current brightness value. 
		"""
		pass

	@overload
	def setBrightness(self, gamma: float) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			gamma: the new brightness value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getCloudsMode(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current cloud rendering mode. 
		"""
		pass

	@overload
	def setCloudsMode(self, mode: str) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the cloud rendering mode to select. Must be either "off", "fast" or "fancy" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isFullscreen(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the game is running in fullscreen mode, 'false' otherwise. 
		"""
		pass

	@overload
	def setFullScreen(self, fullscreen: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			fullscreen: whether to enable fullscreen mode or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getParticleMode(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the current particle rendering mode. 
		"""
		pass

	@overload
	def setParticleMode(self, mode: str) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			mode: the particle rendering mode to select. Must be either "minimal", "decreased"
            or "all" 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getMipMapLevels(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the current mip map level. 
		"""
		pass

	@overload
	def setMipMapLevels(self, val: int) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new mip map level 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def areEntityShadowsEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if entity shadows should be rendered, 'false' otherwise. 
		"""
		pass

	@overload
	def enableEntityShadows(self, val: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: whether to enable entity shadows or not 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getDistortionEffect(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current distortion effect scale. 
		"""
		pass

	@overload
	def setDistortionEffects(self, val: float) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new distortion effect scale 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getEntityDistance(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current entity render distance. 
		"""
		pass

	@overload
	def setEntityDistance(self, val: float) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new entity render distance 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getFovEffects(self) -> float:
		"""
		Since: 1.8.4 

		Returns:
			the current fov value. 
		"""
		pass

	@overload
	def setFovEffects(self, val: float) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Args:
			val: the new fov value 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def isAutosaveIndicatorEnabled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the autosave indicator is enabled, 'false' otherwise. 
		"""
		pass

	@overload
	def enableAutosaveIndicator(self, val: bool) -> "OptionsHelper_VideoOptionsHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	pass


