from typing import overload
from typing import List
from typing import TypeVar
from .IScreen import IScreen
from .IScreenInternal import IScreenInternal
from .Draw2DElement import Draw2DElement
from .Draw2D import Draw2D
from .Line import Line
from .Text import Text
from .Rect import Rect
from .Item import Item
from .Image import Image
from .TextFieldWidgetHelper import TextFieldWidgetHelper
from .ClickableWidgetHelper import ClickableWidgetHelper
from .RenderElement import RenderElement
from .TextHelper import TextHelper
from .ItemStackHelper import ItemStackHelper
from .MethodWrapper import MethodWrapper
from .CheckBoxWidgetHelper import CheckBoxWidgetHelper
from .SliderWidgetHelper import SliderWidgetHelper
from .LockButtonWidgetHelper import LockButtonWidgetHelper
from .CyclingButtonWidgetHelper import CyclingButtonWidgetHelper
from .ButtonWidgetHelper_ButtonBuilder import ButtonWidgetHelper_ButtonBuilder
from .CheckBoxWidgetHelper_CheckBoxBuilder import CheckBoxWidgetHelper_CheckBoxBuilder
from .CyclingButtonWidgetHelper_CyclicButtonBuilder import CyclingButtonWidgetHelper_CyclicButtonBuilder
from .LockButtonWidgetHelper_LockButtonBuilder import LockButtonWidgetHelper_LockButtonBuilder
from .SliderWidgetHelper_SliderBuilder import SliderWidgetHelper_SliderBuilder
from .TextFieldWidgetHelper_TextFieldBuilder import TextFieldWidgetHelper_TextFieldBuilder
from .ButtonWidgetHelper_TexturedButtonBuilder import ButtonWidgetHelper_TexturedButtonBuilder

net_minecraft_client_gui_AbstractParentElement = TypeVar("net_minecraft_client_gui_AbstractParentElement")
AbstractParentElement = net_minecraft_client_gui_AbstractParentElement

T = TypeVar("T")
org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_ = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_")
CallbackInfoReturnable = org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Style = TypeVar("net_minecraft_text_Style")
Style = net_minecraft_text_Style

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class MixinScreen(IScreen, IScreenInternal, AbstractParentElement):
	width: int
	height: int
	textRenderer: TextRenderer

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onClose(self) -> None:
		pass

	@overload
	def tick(self) -> None:
		pass

	@overload
	def handleTextClick(self, style: Style) -> bool:
		pass

	@overload
	def getWidth(self) -> int:
		pass

	@overload
	def getHeight(self) -> int:
		pass

	@overload
	def getDraw2Ds(self) -> List[Draw2DElement]:
		pass

	@overload
	def addDraw2D(self, draw2D: Draw2D, x: int, y: int, width: int, height: int) -> Draw2DElement:
		pass

	@overload
	def addDraw2D(self, draw2D: Draw2D, x: int, y: int, width: int, height: int, zIndex: int) -> Draw2DElement:
		pass

	@overload
	def removeDraw2D(self, draw2D: Draw2DElement) -> IScreen:
		pass

	@overload
	def getLines(self) -> List[Line]:
		pass

	@overload
	def getTexts(self) -> List[Text]:
		pass

	@overload
	def getRects(self) -> List[Rect]:
		pass

	@overload
	def getItems(self) -> List[Item]:
		pass

	@overload
	def getImages(self) -> List[Image]:
		pass

	@overload
	def getTextFields(self) -> List[TextFieldWidgetHelper]:
		pass

	@overload
	def getButtonWidgets(self) -> List[ClickableWidgetHelper]:
		pass

	@overload
	def getElements(self) -> List[RenderElement]:
		pass

	@overload
	def removeElement(self, e: RenderElement) -> IScreen:
		pass

	@overload
	def reAddElement(self, e: T) -> T:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def addText(self, text: str, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def addText(self, text: TextHelper, x: int, y: int, color: int, zIndex: int, shadow: bool, scale: float, rotation: float) -> Text:
		pass

	@overload
	def removeText(self, t: Text) -> IScreen:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int) -> Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.4.0 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def addImage(self, x: int, y: int, width: int, height: int, zIndex: int, alpha: int, color: int, id: str, imageX: int, imageY: int, regionWidth: int, regionHeight: int, textureWidth: int, textureHeight: int, rotation: float) -> Image:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def removeImage(self, i: Image) -> IScreen:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int) -> Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float) -> Rect:
		pass

	@overload
	def addRect(self, x1: int, y1: int, x2: int, y2: int, color: int, alpha: int, rotation: float, zIndex: int) -> Rect:
		pass

	@overload
	def removeRect(self, r: Rect) -> IScreen:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, width: float, rotation: float) -> Line:
		pass

	@overload
	def addLine(self, x1: int, y1: int, x2: int, y2: int, color: int, zIndex: int, width: float, rotation: float) -> Line:
		pass

	@overload
	def removeLine(self, l: Line) -> IScreen:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, id: str, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def addItem(self, x: int, y: int, zIndex: int, item: ItemStackHelper, overlay: bool, scale: float, rotation: float) -> Item:
		pass

	@overload
	def removeItem(self, i: Item) -> IScreen:
		pass

	@overload
	def getScreenClassName(self) -> str:
		pass

	@overload
	def getTitleText(self) -> str:
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, text: str, callback: MethodWrapper) -> ClickableWidgetHelper:
		pass

	@overload
	def addButton(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, callback: MethodWrapper) -> ClickableWidgetHelper:
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, text: str, checked: bool, showMessage: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, text: str, checked: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, checked: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		pass

	@overload
	def addCheckbox(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, checked: bool, showMessage: bool, callback: MethodWrapper) -> CheckBoxWidgetHelper:
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, text: str, value: float, steps: int, callback: MethodWrapper) -> SliderWidgetHelper:
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, value: float, callback: MethodWrapper) -> SliderWidgetHelper:
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, text: str, value: float, callback: MethodWrapper) -> SliderWidgetHelper:
		pass

	@overload
	def addSlider(self, x: int, y: int, width: int, height: int, zIndex: int, text: str, value: float, steps: int, callback: MethodWrapper) -> SliderWidgetHelper:
		pass

	@overload
	def addLockButton(self, x: int, y: int, callback: MethodWrapper) -> LockButtonWidgetHelper:
		pass

	@overload
	def addLockButton(self, x: int, y: int, zIndex: int, callback: MethodWrapper) -> LockButtonWidgetHelper:
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, values: List[str], initial: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], initial: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], alternatives: List[str], initial: str, prefix: str, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		pass

	@overload
	def addCyclingButton(self, x: int, y: int, width: int, height: int, zIndex: int, values: List[str], alternatives: List[str], initial: str, prefix: str, alternateToggle: MethodWrapper, callback: MethodWrapper) -> CyclingButtonWidgetHelper:
		pass

	@overload
	def removeButton(self, btn: ClickableWidgetHelper) -> IScreen:
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		pass

	@overload
	def addTextInput(self, x: int, y: int, width: int, height: int, zIndex: int, message: str, onChange: MethodWrapper) -> TextFieldWidgetHelper:
		pass

	@overload
	def removeTextInput(self, inp: TextFieldWidgetHelper) -> IScreen:
		pass

	@overload
	def soft$close(self) -> None:
		pass

	@overload
	def setOnMouseDown(self, onMouseDown: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnMouseDrag(self, onMouseDrag: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnMouseUp(self, onMouseUp: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnScroll(self, onScroll: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnKeyPressed(self, onKeyPressed: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnCharTyped(self, onCharTyped: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnInit(self, onInit: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnFailInit(self, catchInit: MethodWrapper) -> IScreen:
		pass

	@overload
	def setOnClose(self, onClose: MethodWrapper) -> IScreen:
		pass

	@overload
	def reloadScreen(self) -> IScreen:
		pass

	@overload
	def buttonBuilder(self) -> ButtonWidgetHelper_ButtonBuilder:
		pass

	@overload
	def checkBoxBuilder(self) -> CheckBoxWidgetHelper_CheckBoxBuilder:
		pass

	@overload
	def checkBoxBuilder(self, checked: bool) -> CheckBoxWidgetHelper_CheckBoxBuilder:
		pass

	@overload
	def cyclicButtonBuilder(self, valueToText: MethodWrapper) -> CyclingButtonWidgetHelper_CyclicButtonBuilder:
		pass

	@overload
	def lockButtonBuilder(self) -> LockButtonWidgetHelper_LockButtonBuilder:
		pass

	@overload
	def lockButtonBuilder(self, locked: bool) -> LockButtonWidgetHelper_LockButtonBuilder:
		pass

	@overload
	def sliderBuilder(self) -> SliderWidgetHelper_SliderBuilder:
		pass

	@overload
	def textFieldBuilder(self) -> TextFieldWidgetHelper_TextFieldBuilder:
		pass

	@overload
	def texturedButtonBuilder(self) -> ButtonWidgetHelper_TexturedButtonBuilder:
		pass

	@overload
	def jsmacros_render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def jsmacros_mouseClicked(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> None:
		pass

	@overload
	def jsmacros_mouseReleased(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> None:
		pass

	@overload
	def jsmacros_charTyped(self, chr: str, modifiers: int) -> None:
		pass

	@overload
	def jsmacros_mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> None:
		pass

	@overload
	def handleCustomClickEvent(self, style: Style, cir: CallbackInfoReturnable) -> None:
		pass

	@overload
	def getOnClose(self) -> MethodWrapper:
		pass

	pass


