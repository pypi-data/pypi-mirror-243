from typing import overload
from typing import List
from typing import Mapping
from .HTTPRequest_Response import HTTPRequest_Response


class HTTPRequest:
	"""
	Since: 1.1.8 
	"""
	headers: Mapping[str, str]
	conn: URL
	connectTimeout: int
	readTimeout: int

	@overload
	def __init__(self, url: str) -> None:
		pass

	@overload
	def addHeader(self, key: str, value: str) -> "HTTPRequest":
		"""
		Since: 1.1.8 

		Args:
			value: 
			key: 
		"""
		pass

	@overload
	def setConnectTimeout(self, timeout: int) -> "HTTPRequest":
		"""
		Since: 1.8.6 
		"""
		pass

	@overload
	def setReadTimeout(self, timeout: int) -> "HTTPRequest":
		"""
		Since: 1.8.6 
		"""
		pass

	@overload
	def get(self) -> HTTPRequest_Response:
		"""
		Since: 1.1.8 
		"""
		pass

	@overload
	def post(self, data: str) -> HTTPRequest_Response:
		"""
		Since: 1.1.8 

		Args:
			data: 
		"""
		pass

	@overload
	def post(self, data: List[float]) -> HTTPRequest_Response:
		"""
		Since: 1.8.4 

		Args:
			data: 
		"""
		pass

	@overload
	def put(self, data: str) -> HTTPRequest_Response:
		"""
		Since: 1.8.4 

		Args:
			data: 
		"""
		pass

	@overload
	def put(self, data: List[float]) -> HTTPRequest_Response:
		"""
		Since: 1.8.4 

		Args:
			data: 
		"""
		pass

	@overload
	def send(self, method: str) -> HTTPRequest_Response:
		"""
		Since: 1.8.6 
		"""
		pass

	@overload
	def send(self, method: str, data: str) -> HTTPRequest_Response:
		"""
		Since: 1.8.4 

		Args:
			method: 
			data: 
		"""
		pass

	@overload
	def send(self, method: str, data: List[float]) -> HTTPRequest_Response:
		"""
		Since: 1.8.4 

		Args:
			method: 
			data: 
		"""
		pass

	pass


