from typing import overload
from typing import TypeVar

com_neovisionaries_ws_client_WebSocketFrame = TypeVar("com_neovisionaries_ws_client_WebSocketFrame")
WebSocketFrame = com_neovisionaries_ws_client_WebSocketFrame


class Websocket_Disconnected:
	"""
	"""
	serverFrame: WebSocketFrame
	clientFrame: WebSocketFrame
	isServer: bool

	@overload
	def __init__(self, serverFrame: WebSocketFrame, clientFrame: WebSocketFrame, isServer: bool) -> None:
		"""

		Args:
			isServer: 
			clientFrame: 
			serverFrame: 
		"""
		pass

	pass


