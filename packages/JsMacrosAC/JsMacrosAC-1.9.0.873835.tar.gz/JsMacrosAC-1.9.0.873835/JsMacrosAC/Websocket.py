from typing import overload
from typing import TypeVar
from .MethodWrapper import MethodWrapper

com_neovisionaries_ws_client_WebSocket = TypeVar("com_neovisionaries_ws_client_WebSocket")
WebSocket = com_neovisionaries_ws_client_WebSocket


class Websocket:
	"""
	"""
	onConnect: MethodWrapper
	onTextMessage: MethodWrapper
	onDisconnect: MethodWrapper
	onError: MethodWrapper
	onFrame: MethodWrapper

	@overload
	def __init__(self, address: str) -> None:
		pass

	@overload
	def __init__(self, address: URL) -> None:
		pass

	@overload
	def connect(self) -> "Websocket":
		"""
		Since: 1.1.9 

		Returns:
			self 
		"""
		pass

	@overload
	def getWs(self) -> WebSocket:
		"""
		Since: 1.1.9 
		"""
		pass

	@overload
	def sendText(self, text: str) -> "Websocket":
		"""
		Since: 1.1.9 

		Args:
			text: 

		Returns:
			self 
		"""
		pass

	@overload
	def close(self) -> "Websocket":
		"""
		Since: 1.1.9 

		Returns:
			self 
		"""
		pass

	@overload
	def close(self, closeCode: int) -> "Websocket":
		"""
		Since: 1.1.9 

		Args:
			closeCode: 

		Returns:
			self 
		"""
		pass

	pass


