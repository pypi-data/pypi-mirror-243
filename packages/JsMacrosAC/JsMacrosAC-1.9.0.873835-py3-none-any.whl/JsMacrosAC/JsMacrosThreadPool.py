from typing import overload
from typing import TypeVar

java_util_function_Consumer_java_lang_Thread_ = TypeVar("java_util_function_Consumer_java_lang_Thread_")
Consumer = java_util_function_Consumer_java_lang_Thread_

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class JsMacrosThreadPool:
	maxFreeThreads: int

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def __init__(self, maxFreeThreads: int) -> None:
		pass

	@overload
	def runTask(self, task: Runnable) -> Thread:
		pass

	@overload
	def runTask(self, task: Runnable, beforeRunTask: Consumer) -> Thread:
		pass

	pass


