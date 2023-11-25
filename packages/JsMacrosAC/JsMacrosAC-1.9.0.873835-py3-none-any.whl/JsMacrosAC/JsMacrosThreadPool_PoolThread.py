from typing import overload
from typing import TypeVar

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class JsMacrosThreadPool_PoolThread(Thread):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def runTask(self, task: Runnable) -> None:
		pass

	@overload
	def run(self) -> None:
		pass

	pass


