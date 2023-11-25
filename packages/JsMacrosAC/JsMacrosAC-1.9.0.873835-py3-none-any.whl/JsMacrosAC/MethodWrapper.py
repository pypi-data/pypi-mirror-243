from typing import overload
from typing import TypeVar
from typing import Generic

C = TypeVar("C")
C = C

java_util_function_Predicate_T_ = TypeVar("java_util_function_Predicate_T_")
Predicate = java_util_function_Predicate_T_

java_util_Comparator_T_ = TypeVar("java_util_Comparator_T_")
Comparator = java_util_Comparator_T_

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread

java_util_function_Function_ super R, extends V_ = TypeVar("java_util_function_Function_ super R, extends V_")
Function = java_util_function_Function_ super R, extends V_

R = TypeVar("R")
T = TypeVar("T")
java_util_function_Consumer_T_ = TypeVar("java_util_function_Consumer_T_")
Consumer = java_util_function_Consumer_T_

U = TypeVar("U")
java_util_function_BiFunction_T,U,R_ = TypeVar("java_util_function_BiFunction_T,U,R_")
BiFunction = java_util_function_BiFunction_T,U,R_

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable

java_util_function_Supplier_R_ = TypeVar("java_util_function_Supplier_R_")
Supplier = java_util_function_Supplier_R_

java_util_function_BiConsumer_T,U_ = TypeVar("java_util_function_BiConsumer_T,U_")
BiConsumer = java_util_function_BiConsumer_T,U_

java_util_function_BiPredicate_T,U_ = TypeVar("java_util_function_BiPredicate_T,U_")
BiPredicate = java_util_function_BiPredicate_T,U_


class MethodWrapper(Consumer, BiConsumer, Function, BiFunction, Predicate, BiPredicate, Runnable, Supplier, Comparator, Generic[T, U, R, C]):
	"""Wraps most of the important functional interfaces.
	"""

	@overload
	def __init__(self, containingContext: C) -> None:
		pass

	@overload
	def getCtx(self) -> C:
		pass

	@overload
	def accept(self, t: T) -> None:
		pass

	@overload
	def accept(self, t: T, u: U) -> None:
		pass

	@overload
	def apply(self, t: T) -> R:
		pass

	@overload
	def apply(self, t: T, u: U) -> R:
		pass

	@overload
	def test(self, t: T) -> bool:
		pass

	@overload
	def test(self, t: T, u: U) -> bool:
		pass

	@overload
	def preventSameScriptJoin(self) -> bool:
		"""override to return true if the method can't join to the context it was wrapped/created in, ie for languages that don't allow multithreading.
		"""
		pass

	@overload
	def overrideThread(self) -> Thread:
		"""make return something to override the thread set in FJsMacros#on(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) (hi jep)
		"""
		pass

	@overload
	def andThen(self, after: Function) -> "MethodWrapper":
		"""Makes Function and BiFunction work together.
Extended so it's called on every type not just those 2.

		Args:
			after: put a MethodWrapper here when using in scripts. 
		"""
		pass

	@overload
	def negate(self) -> "MethodWrapper":
		"""Makes Predicate and BiPredicate work together
		"""
		pass

	pass


