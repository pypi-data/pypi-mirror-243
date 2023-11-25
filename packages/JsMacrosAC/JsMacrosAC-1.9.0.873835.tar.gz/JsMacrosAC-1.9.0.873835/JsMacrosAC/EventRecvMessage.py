from typing import overload
from typing import List
from typing import TypeVar
from .BaseEvent import BaseEvent
from .TextHelper import TextHelper

net_minecraft_client_gui_hud_MessageIndicator = TypeVar("net_minecraft_client_gui_hud_MessageIndicator")
MessageIndicator = net_minecraft_client_gui_hud_MessageIndicator

net_minecraft_network_message_MessageSignatureData = TypeVar("net_minecraft_network_message_MessageSignatureData")
MessageSignatureData = net_minecraft_network_message_MessageSignatureData

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class EventRecvMessage(BaseEvent):
	"""
	Since: 1.2.7 
	"""
	text: TextHelper
	signature: List[float]
	messageType: str

	@overload
	def __init__(self, message: Text, signature: MessageSignatureData, indicator: MessageIndicator) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


