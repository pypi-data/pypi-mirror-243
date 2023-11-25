from typing import overload
from typing import List
from typing import TypeVar
from .Box import Box
from .Line3D import Line3D
from .TraceLine import TraceLine
from .EntityTraceLine import EntityTraceLine
from .Surface import Surface
from .RenderElement3D import RenderElement3D
from .Pos3D import Pos3D
from .EntityHelper import EntityHelper
from .Box_Builder import Box_Builder
from .BlockPosHelper import BlockPosHelper
from .Line3D_Builder import Line3D_Builder
from .TraceLine_Builder import TraceLine_Builder
from .EntityTraceLine_Builder import EntityTraceLine_Builder
from .Surface_Builder import Surface_Builder

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext


class Draw3D:
	"""Draw2D is cool\n
	Since: 1.0.6 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getBoxes(self) -> List[Box]:
		"""
		Since: 1.0.6 
		"""
		pass

	@overload
	def getLines(self) -> List[Line3D]:
		"""
		Since: 1.0.6 
		"""
		pass

	@overload
	def getTraceLines(self) -> List[TraceLine]:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def getEntityTraceLines(self) -> List[EntityTraceLine]:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def getDraw2Ds(self) -> List[Surface]:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def clear(self) -> None:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def reAddElement(self, element: RenderElement3D) -> None:
		"""
		Since: 1.8.4 

		Args:
			element: 
		"""
		pass

	@overload
	def addBox(self, box: Box) -> None:
		"""
		Since: 1.8.4 

		Args:
			box: 
		"""
		pass

	@overload
	def addLine(self, line: Line3D) -> None:
		"""
		Since: 1.8.4 

		Args:
			line: 
		"""
		pass

	@overload
	def addTraceLine(self, line: TraceLine) -> None:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addSurface(self, surface: Surface) -> None:
		"""
		Since: 1.8.4 

		Args:
			surface: 
		"""
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, fillColor: int, fill: bool) -> Box:
		"""
		Since: 1.0.6 

		Args:
			fillColor: 
			color: 
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
			fill: 

		Returns:
			The Box you added. 
		"""
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, fillColor: int, fill: bool, cull: bool) -> Box:
		"""
		Since: 1.3.1 

		Args:
			fillColor: 
			color: 
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
			fill: 
			cull: 
		"""
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, fillColor: int, fillAlpha: int, fill: bool) -> Box:
		"""
		Since: 1.1.8 

		Args:
			fillColor: 
			color: 
			z1: 
			alpha: 
			y1: 
			z2: 
			x1: 
			y2: 
			fillAlpha: 
			x2: 
			fill: 

		Returns:
			the Box you added. 
		"""
		pass

	@overload
	def addBox(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, fillColor: int, fillAlpha: int, fill: bool, cull: bool) -> Box:
		pass

	@overload
	def removeBox(self, b: Box) -> "Draw3D":
		"""
		Since: 1.0.6 

		Args:
			b: 
		"""
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int) -> Line3D:
		"""
		Since: 1.0.6 

		Args:
			color: 
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 

		Returns:
			the Line3D you added. 
		"""
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, cull: bool) -> Line3D:
		"""
		Since: 1.3.1 

		Args:
			color: 
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
			cull: 
		"""
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int) -> Line3D:
		"""
		Since: 1.1.8 

		Args:
			color: 
			z1: 
			alpha: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 

		Returns:
			the Line3D you added. 
		"""
		pass

	@overload
	def addLine(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, cull: bool) -> Line3D:
		"""
		Since: 1.3.1 

		Args:
			color: 
			z1: 
			alpha: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
			cull: 
		"""
		pass

	@overload
	def removeLine(self, l: Line3D) -> "Draw3D":
		"""
		Since: 1.0.6 

		Args:
			l: 
		"""
		pass

	@overload
	def addTraceLine(self, x: float, y: float, z: float, color: int) -> TraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addTraceLine(self, x: float, y: float, z: float, color: int, alpha: int) -> TraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addTraceLine(self, pos: Pos3D, color: int) -> TraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addTraceLine(self, pos: Pos3D, color: int, alpha: int) -> TraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addEntityTraceLine(self, entity: EntityHelper, color: int) -> EntityTraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addEntityTraceLine(self, entity: EntityHelper, color: int, alpha: int) -> EntityTraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def addEntityTraceLine(self, entity: EntityHelper, color: int, alpha: int, yOffset: float) -> EntityTraceLine:
		"""
		Since: 1.9.0 
		"""
		pass

	@overload
	def removeTraceLine(self, traceLine: TraceLine) -> "Draw3D":
		"""
		Since: 1.9.0 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def addPoint(self, point: Pos3D, radius: float, color: int) -> Box:
		"""Draws a cube( Box ) with a specific radius( 'side length = 2*radius' )\n
		Since: 1.4.0 

		Args:
			color: point color 
			radius: 1/2 of the side length of the cube 
			point: the center point 

		Returns:
			the Box generated, and visualized 
		"""
		pass

	@overload
	def addPoint(self, x: float, y: float, z: float, radius: float, color: int) -> Box:
		"""Draws a cube( Box ) with a specific radius( 'side length = 2*radius' )\n
		Since: 1.4.0 

		Args:
			color: point color 
			x: x value of the center point 
			y: y value of the center point 
			z: z value of the center point 
			radius: 1/2 of the side length of the cube 

		Returns:
			the Box generated, and visualized 
		"""
		pass

	@overload
	def addPoint(self, x: float, y: float, z: float, radius: float, color: int, alpha: int, cull: bool) -> Box:
		"""Draws a cube( Box ) with a specific radius( 'side length = 2*radius' )\n
		Since: 1.4.0 

		Args:
			color: point color 
			alpha: alpha of the point 
			x: x value of the center point 
			y: y value of the center point 
			z: z value of the center point 
			radius: 1/2 of the side length of the cube 
			cull: whether to cull the point or not 

		Returns:
			the Box generated, and visualized 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			x: top left 
			y: 
			z: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, width: float, height: float) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			x: 
			width: 
			y: 
			z: 
			height: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, xRot: float, yRot: float, zRot: float) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			zRot: 
			yRot: 
			x: 
			xRot: 
			y: 
			z: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, xRot: float, yRot: float, zRot: float, width: float, height: float) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			zRot: 
			yRot: 
			x: 
			xRot: 
			width: 
			y: 
			z: 
			height: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, xRot: float, yRot: float, zRot: float, width: float, height: float, minSubdivisions: int) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			zRot: 
			yRot: 
			x: 
			xRot: 
			width: 
			y: 
			z: 
			minSubdivisions: 
			height: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, xRot: float, yRot: float, zRot: float, width: float, height: float, minSubdivisions: int, renderBack: bool) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			zRot: 
			yRot: 
			x: 
			xRot: 
			width: 
			y: 
			z: 
			minSubdivisions: 
			renderBack: 
			height: 
		"""
		pass

	@overload
	def addDraw2D(self, x: float, y: float, z: float, xRot: float, yRot: float, zRot: float, width: float, height: float, minSubdivisions: int, renderBack: bool, cull: bool) -> Surface:
		"""
		Since: 1.6.5 

		Args:
			zRot: 
			yRot: 
			x: top left 
			xRot: 
			width: 
			y: 
			z: 
			minSubdivisions: 
			renderBack: 
			height: 
		"""
		pass

	@overload
	def removeDraw2D(self, surface: Surface) -> None:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def boxBuilder(self) -> Box_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a new Box_Builder instance. 
		"""
		pass

	@overload
	def boxBuilder(self, pos: BlockPosHelper) -> Box_Builder:
		"""
		Since: 1.8.4 

		Args:
			pos: the block position of the box 

		Returns:
			a new Box_Builder instance. 
		"""
		pass

	@overload
	def boxBuilder(self, x: int, y: int, z: int) -> Box_Builder:
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate of the box 
			y: the y coordinate of the box 
			z: the z coordinate of the box 

		Returns:
			a new Box_Builder instance. 
		"""
		pass

	@overload
	def lineBuilder(self) -> Line3D_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a new Line3D_Builder instance. 
		"""
		pass

	@overload
	def traceLineBuilder(self) -> TraceLine_Builder:
		"""
		Since: 1.9.0 

		Returns:
			a new TraceLine_Builder instance. 
		"""
		pass

	@overload
	def entityTraceLineBuilder(self) -> EntityTraceLine_Builder:
		"""
		Since: 1.9.0 

		Returns:
			a new EntityTraceLine_Builder instance. 
		"""
		pass

	@overload
	def surfaceBuilder(self) -> Surface_Builder:
		"""
		Since: 1.8.4 

		Returns:
			a new Surface_Builder instance. 
		"""
		pass

	@overload
	def register(self) -> "Draw3D":
		"""register so it actually shows up\n
		Since: 1.6.5 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def unregister(self) -> "Draw3D":
		"""
		Since: 1.6.5 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def render(self, drawContext: DrawContext, tickDelta: float) -> None:
		pass

	pass


