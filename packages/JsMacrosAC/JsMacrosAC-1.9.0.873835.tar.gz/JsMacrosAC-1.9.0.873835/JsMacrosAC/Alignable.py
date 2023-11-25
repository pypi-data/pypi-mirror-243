from typing import overload
from typing import TypeVar

B = TypeVar("B")
B = B


class Alignable:
	"""
	Since: 1.8.4 
	"""

	@overload
	def alignHorizontally(self, other: "Alignable", alignment: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			other: the element to align to 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignHorizontally(self, other: "Alignable", alignment: str, offset: int) -> B:
		"""The alignment must be of the format '[left|center|right|x%]On[left|center|right|x%]' . The input is case-insensitive.
The first alignment is for the element this method is called on and the second is for the
other element. As an example, 'LeftOnCenter' would align the left side of this
element to the center of the other element.\n
		Since: 1.8.4 

		Args:
			other: the element to align to 
			offset: the offset to use 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignHorizontally(self, alignment: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignHorizontally(self, alignment: str, offset: int) -> B:
		"""Possible alignments are 'left' , 'center' , 'right' or 'y%' where y
is a number between 0 and 100.\n
		Since: 1.8.4 

		Args:
			offset: the offset to use 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignVertically(self, other: "Alignable", alignment: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			other: the element to align to 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignVertically(self, other: "Alignable", alignment: str, offset: int) -> B:
		"""The alignment must be of the format '[top|center|bottom|y%]On[top|center|bottom|y%]' . The input is case-insensitive.
The first alignment is for the element this method is called on and the second is for the
other element. As an example, 'BottomOnTop' would align the bottom side of this
element to the top of the other element. Thus, the element would be placed above the
other one.\n
		Since: 1.8.4 

		Args:
			other: the element to align to 
			offset: the offset to use 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignVertically(self, alignment: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def alignVertically(self, alignment: str, offset: int) -> B:
		"""Possible alignments are 'top' , 'center' , 'bottom' or 'x%' where x
is a number between 0 and 100.\n
		Since: 1.8.4 

		Args:
			offset: the offset to use 
			alignment: the alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def align(self, horizontal: str, vertical: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			horizontal: the horizontal alignment to use 
			vertical: the vertical alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def align(self, horizontal: str, horizontalOffset: int, vertical: str, verticalOffset: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			horizontal: the horizontal alignment to use 
			verticalOffset: the vertical offset to use 
			vertical: the vertical alignment to use 
			horizontalOffset: the horizontal offset to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def align(self, other: "Alignable", horizontal: str, vertical: str) -> B:
		"""
		Since: 1.8.4 

		Args:
			horizontal: the horizontal alignment to use 
			other: the element to align to 
			vertical: the vertical alignment to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def align(self, other: "Alignable", horizontal: str, horizontalOffset: int, vertical: str, verticalOffset: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			horizontal: the horizontal alignment to use 
			other: the element to align to 
			verticalOffset: the vertical offset to use 
			vertical: the vertical alignment to use 
			horizontalOffset: the horizontal offset to use 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def moveTo(self, x: int, y: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			x: the new x position 
			y: the new y position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def moveToX(self, x: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			x: the new x position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def moveToY(self, y: int) -> B:
		"""
		Since: 1.8.4 

		Args:
			y: the new y position 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getScaledWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the scaled width of the element. 
		"""
		pass

	@overload
	def getParentWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the parent element. 
		"""
		pass

	@overload
	def getScaledHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the scaled height of the element. 
		"""
		pass

	@overload
	def getParentHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the parent element. 
		"""
		pass

	@overload
	def getScaledLeft(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the position of the scaled element's left side. 
		"""
		pass

	@overload
	def getScaledTop(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the position of the scaled element's top side. 
		"""
		pass

	@overload
	def getScaledRight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the position of the scaled element's right side. 
		"""
		pass

	@overload
	def getScaledBottom(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the position of the scaled element's bottom side. 
		"""
		pass

	@overload
	def parsePercentage(self, string: str) -> int:
		"""Parse the string containing a percentage of the form 'x%' and return its value.\n
		Since: 1.8.4 

		Args:
			string: the string to parse 

		Returns:
			the percentage or '-1' if the string is not a valid percentage. 
		"""
		pass

	pass


