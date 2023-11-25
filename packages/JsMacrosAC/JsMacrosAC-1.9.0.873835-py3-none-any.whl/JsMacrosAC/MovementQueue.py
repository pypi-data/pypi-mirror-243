from typing import overload
from typing import TypeVar
from .Draw3D import Draw3D
from .PlayerInput import PlayerInput

net_minecraft_client_network_ClientPlayerEntity = TypeVar("net_minecraft_client_network_ClientPlayerEntity")
ClientPlayerEntity = net_minecraft_client_network_ClientPlayerEntity


class MovementQueue:
	predPoints: Draw3D

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def tick(self, newPlayer: ClientPlayerEntity) -> PlayerInput:
		pass

	@overload
	def append(self, input: PlayerInput, newPlayer: ClientPlayerEntity) -> None:
		pass

	@overload
	def setDrawPredictions(self, val: bool) -> None:
		pass

	@overload
	def clear(self) -> None:
		pass

	pass


