from typing import TypeVar

from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .FChat import FChat
from .FPlayer import FPlayer
from .FRequest import FRequest
from .FJavaUtils import FJavaUtils
from .FHud import FHud
from .FKeyBind import FKeyBind
from .FTime import FTime
from .FJsMacros import FJsMacros
from .FFS import FFS
from .FReflection import FReflection
from .FUtils import FUtils
from .FWorld import FWorld
from .FClient import FClient
from .FGlobalVars import FGlobalVars
from .IFWrapper import IFWrapper
from .FPositionCommon import FPositionCommon

File = TypeVar("java.io.File")



Chat = FChat()
Player = FPlayer()
Request = FRequest()
JavaUtils = FJavaUtils()
Hud = FHud()
KeyBind = FKeyBind()
Time = FTime()
JsMacros = FJsMacros()
FS = FFS()
Reflection = FReflection()
Utils = FUtils()
World = FWorld()
Client = FClient()
GlobalVars = FGlobalVars()
JavaWrapper = IFWrapper()
PositionCommon = FPositionCommon()
context = EventContainer()
file = File()
event = BaseEvent()
