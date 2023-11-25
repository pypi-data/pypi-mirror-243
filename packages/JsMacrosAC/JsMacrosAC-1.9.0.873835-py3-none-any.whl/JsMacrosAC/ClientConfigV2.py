from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Sorting_MacroSortMethod import Sorting_MacroSortMethod
from .Sorting_ServiceSortMethod import Sorting_ServiceSortMethod

com_google_gson_JsonObject = TypeVar("com_google_gson_JsonObject")
JsonObject = com_google_gson_JsonObject

java_util_Comparator_java_lang_String_ = TypeVar("java_util_Comparator_java_lang_String_")
Comparator = java_util_Comparator_java_lang_String_


class ClientConfigV2:
	sortMethod: Sorting_MacroSortMethod
	sortServicesMethod: Sorting_ServiceSortMethod
	showSlotIndexes: bool
	disableKeyWhenScreenOpen: bool
	editorTheme: Mapping[str, List[float]]
	editorLinterOverrides: Mapping[str, str]
	editorHistorySize: int
	editorSuggestions: bool
	editorFont: str
	externalEditor: bool
	externalEditorCommand: str
	showRunningServices: bool
	serviceAutoReload: bool

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def languages(self) -> List[str]:
		pass

	@overload
	def getFonts(self) -> List[str]:
		pass

	@overload
	def getThemeData(self) -> Mapping[str, List[float]]:
		pass

	@overload
	def setServiceAutoReload(self, value: bool) -> None:
		pass

	@overload
	def getSortComparator(self) -> Comparator:
		pass

	@overload
	def getServiceSortComparator(self) -> Comparator:
		pass

	@overload
	def fromV1(self, v1: JsonObject) -> None:
		pass

	pass


