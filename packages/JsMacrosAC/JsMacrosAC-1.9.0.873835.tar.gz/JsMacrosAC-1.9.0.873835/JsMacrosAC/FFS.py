from typing import overload
from typing import List
from typing import TypeVar
from .PerExecLibrary import PerExecLibrary
from .BaseScriptContext import BaseScriptContext
from .FileHandler import FileHandler
from .MethodWrapper import MethodWrapper

java_io_File = TypeVar("java_io_File")
File = java_io_File


class FFS(PerExecLibrary):
	"""Better File-System functions. 
An instance of this class is passed to scripts as the 'FS' variable.\n
	Since: 1.1.8 
	"""

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def list(self, path: str) -> List[str]:
		"""List files in path.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 

		Returns:
			An array of file names as String . 
		"""
		pass

	@overload
	def exists(self, path: str) -> bool:
		"""Check if a file exists.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 
		"""
		pass

	@overload
	def isDir(self, path: str) -> bool:
		"""Check if a file is a directory.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 
		"""
		pass

	@overload
	def isFile(self, path: str) -> bool:
		"""
		Since: 1.8.4 

		Args:
			path: the path relative to the script's folder 

		Returns:
			'true' if the path leads to a file, 'false' otherwise. 
		"""
		pass

	@overload
	def getName(self, path: str) -> str:
		"""Get the last part (name) of a file.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 

		Returns:
			a String of the file name. 
		"""
		pass

	@overload
	def toRelativePath(self, absolutePath: str) -> str:
		"""
		Since: 1.8.4 

		Args:
			absolutePath: the absolute path to the file 

		Returns:
			a path relative to the script's folder to the given absolute path. 
		"""
		pass

	@overload
	def createFile(self, path: str, name: str) -> bool:
		"""Creates a new file in the specified path, relative to the script's folder. This will only
work if the parent directory already exists. See FFS#createFile(java.lang.String,java.lang.String,boolean) to automatically create all parent directories.\n
		Since: 1.8.4 

		Args:
			path: the path relative to the script's folder 
			name: the name of the file 

		Returns:
			'true' if the file was created successfully, 'false' otherwise. 
		"""
		pass

	@overload
	def createFile(self, path: str, name: str, createDirs: bool) -> bool:
		"""Creates a new file in the specified path, relative to the script's folder. Optionally parent
directories can be created if they do not exist.\n
		Since: 1.8.4 

		Args:
			path: the path relative to the script's folder 
			createDirs: whether to create parent directories if they do not exist or not 
			name: the name of the file 

		Returns:
			'true' if the file was created successfully, 'false' otherwise. 
		"""
		pass

	@overload
	def makeDir(self, path: str) -> bool:
		"""Make a directory.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 

		Returns:
			a Boolean for success. 
		"""
		pass

	@overload
	def move(self, from_: str, to: str) -> None:
		"""Move a file.\n
		Since: 1.1.8 

		Args:
			from: relative to the script's folder. 
			to: relative to the script's folder. 
		"""
		pass

	@overload
	def copy(self, from_: str, to: str) -> None:
		"""Copy a file.\n
		Since: 1.1.8 

		Args:
			from: relative to the script's folder. 
			to: relative to the script's folder. 
		"""
		pass

	@overload
	def unlink(self, path: str) -> bool:
		"""Delete a file.\n
		Since: 1.2.9 

		Args:
			path: relative to the script's folder. 

		Returns:
			a Boolean for success. 
		"""
		pass

	@overload
	def combine(self, patha: str, pathb: str) -> str:
		"""Combine 2 paths.\n
		Since: 1.1.8 

		Args:
			patha: path is relative to the script's folder. 
			pathb: 

		Returns:
			a String of the combined path. 
		"""
		pass

	@overload
	def getDir(self, path: str) -> str:
		"""Gets the directory part of a file path, or the parent directory of a folder.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 

		Returns:
			a String of the combined path. 
		"""
		pass

	@overload
	def open(self, path: str) -> FileHandler:
		"""Open a FileHandler for the file at the specified path.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 

		Returns:
			a FileHandler for the file path. 
		"""
		pass

	@overload
	def open(self, path: str, charset: str) -> FileHandler:
		"""Open a FileHandler for the file at the specified path.\n
		Since: 1.8.4 

		Args:
			path: relative to the script's folder. 
			charset: the charset to use for reading/writing the file (default is UTF-8) 

		Returns:
			a FileHandler for the file path. 
		"""
		pass

	@overload
	def walkFiles(self, path: str, maxDepth: int, followLinks: bool, visitor: MethodWrapper) -> None:
		"""An advanced method to walk a directory tree and get some information about the files, as well
as their paths.\n
		Since: 1.8.4 

		Args:
			maxDepth: the maximum depth to follow, can cause stack overflow if too high 
			path: the relative path of the directory to walk through 
			followLinks: whether to follow symbolic links 
			visitor: the visitor that is called for each file with the path of the file and its
                   attributes 
		"""
		pass

	@overload
	def toRawFile(self, path: str) -> File:
		"""
		Since: 1.8.4 

		Args:
			path: the relative path to get the file object for 

		Returns:
			the file object for the specified path. 
		"""
		pass

	@overload
	def toRawPath(self, path: str) -> Path:
		"""
		Since: 1.8.4 

		Args:
			path: the relative path to get the path object for 

		Returns:
			the path object for the specified path. 
		"""
		pass

	@overload
	def getRawAttributes(self, path: str) -> BasicFileAttributes:
		"""
		Since: 1.8.4 

		Args:
			path: the path relative to the script's folder 

		Returns:
			the attributes of the file at the specified path. 
		"""
		pass

	pass


