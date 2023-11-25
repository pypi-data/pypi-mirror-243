from typing import overload
from typing import TypeVar
from .IResourcePackManager import IResourcePackManager

net_minecraft_resource_ResourcePackProfile = TypeVar("net_minecraft_resource_ResourcePackProfile")
ResourcePackProfile = net_minecraft_resource_ResourcePackProfile


class MixinResourcePackManager(IResourcePackManager):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_disableServerPacks(self, disable: bool) -> None:
		pass

	@overload
	def jsmacros_isServerPacksDisabled(self) -> bool:
		pass

	@overload
	def onBuildPackList(self, instance: ResourcePackProfile) -> bool:
		pass

	pass


