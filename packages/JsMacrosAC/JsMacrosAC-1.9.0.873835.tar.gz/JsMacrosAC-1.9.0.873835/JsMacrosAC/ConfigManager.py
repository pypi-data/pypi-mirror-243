from typing import overload
from typing import TypeVar
from typing import Mapping

T = TypeVar("T")
com_google_gson_JsonObject = TypeVar("com_google_gson_JsonObject")
JsonObject = com_google_gson_JsonObject

org_slf4j_Logger = TypeVar("org_slf4j_Logger")
Logger = org_slf4j_Logger

java_io_File = TypeVar("java_io_File")
File = java_io_File


class ConfigManager:
	optionClasses: Mapping[str, Class]
	options: Mapping[Class, object]
	configFolder: File
	macroFolder: File
	configFile: File
	LOGGER: Logger
	rawOptions: JsonObject

	@overload
	def __init__(self, configFolder: File, macroFolder: File, logger: Logger) -> None:
		pass

	@overload
	def reloadRawConfigFromFile(self) -> None:
		pass

	@overload
	def convertConfigFormat(self) -> None:
		pass

	@overload
	def convertConfigFormat(self, clazz: Class) -> None:
		pass

	@overload
	def getOptions(self, optionClass: Class) -> T:
		pass

	@overload
	def addOptions(self, key: str, optionClass: Class) -> None:
		pass

	@overload
	def loadConfig(self) -> None:
		pass

	@overload
	def loadDefaults(self) -> None:
		pass

	@overload
	def saveConfig(self) -> None:
		pass

	pass


