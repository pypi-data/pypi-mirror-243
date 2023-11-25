from typing import overload
from typing import List


class Sorting_ServiceSortMethod:
	"""
	Since: 1.8.4 
	"""
	Name: "Sorting_ServiceSortMethod"
	FileName: "Sorting_ServiceSortMethod"
	Enabled: "Sorting_ServiceSortMethod"
	Running: "Sorting_ServiceSortMethod"

	@overload
	def values(self) -> List["Sorting_ServiceSortMethod"]:
		pass

	@overload
	def valueOf(self, name: str) -> "Sorting_ServiceSortMethod":
		pass

	pass


