from typing import overload
from typing import List
from typing import TypeVar
from .BaseLibrary import BaseLibrary

T = TypeVar("T")
java_util_HashMap_,_ = TypeVar("java_util_HashMap_,_")
HashMap = java_util_HashMap_,_

java_util_ArrayList_T_ = TypeVar("java_util_ArrayList_T_")
ArrayList = java_util_ArrayList_T_

java_util_SplittableRandom = TypeVar("java_util_SplittableRandom")
SplittableRandom = java_util_SplittableRandom

java_util_HashSet__ = TypeVar("java_util_HashSet__")
HashSet = java_util_HashSet__


class FJavaUtils(BaseLibrary):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def createArrayList(self) -> ArrayList:
		"""Creates a java ArrayList .\n
		Since: 1.8.4 

		Returns:
			a java ArrayList. 
		"""
		pass

	@overload
	def createArrayList(self, array: List[T]) -> ArrayList:
		"""Creates a java ArrayList .\n
		Since: 1.8.4 

		Args:
			T: the type of the array 
			array: the array to add to the list 

		Returns:
			a java ArrayList from the given array. 
		"""
		pass

	@overload
	def createHashMap(self) -> HashMap:
		"""Creates a java HashMap .\n
		Since: 1.8.4 

		Returns:
			a java HashMap. 
		"""
		pass

	@overload
	def createHashSet(self) -> HashSet:
		"""Creates a java HashSet .\n
		Since: 1.8.4 

		Returns:
			a java HashSet. 
		"""
		pass

	@overload
	def getRandom(self) -> SplittableRandom:
		"""Returns a SplittableRandom .\n
		Since: 1.8.4 

		Returns:
			a SplittableRandom. 
		"""
		pass

	@overload
	def getRandom(self, seed: float) -> SplittableRandom:
		"""Returns SplittableRandom , initialized with the seed to get identical sequences of
values at all times.\n
		Since: 1.8.4 

		Args:
			seed: the seed 

		Returns:
			a SplittableRandom. 
		"""
		pass

	@overload
	def getHelperFromRaw(self, raw: object) -> object:
		"""
		Since: 1.8.4 

		Args:
			raw: the object to wrap 

		Returns:
			the correct instance of BaseHelper for the given object if it exists and 'null' otherwise. 
		"""
		pass

	@overload
	def arrayToString(self, array: List[object]) -> str:
		"""
		Since: 1.8.4 

		Args:
			array: the array to convert 

		Returns:
			the String representation of the given array. 
		"""
		pass

	@overload
	def arrayDeepToString(self, array: List[object]) -> str:
		"""This method will convert any objects hold in the array data to Strings and should be used for
multidimensional arrays.\n
		Since: 1.8.4 

		Args:
			array: the array to convert 

		Returns:
			the String representation of the given array. 
		"""
		pass

	pass


