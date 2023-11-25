from typing import overload
from typing import List
from typing import TypeVar
from .PerExecLibrary import PerExecLibrary
from .FReflection_CombinedVariableClassLoader import FReflection_CombinedVariableClassLoader
from .BaseScriptContext import BaseScriptContext
from .ProxyBuilder import ProxyBuilder
from .ClassBuilder import ClassBuilder
from .LibraryBuilder import LibraryBuilder
from .Mappings import Mappings
from .WrappedClassInstance import WrappedClassInstance

java_lang_reflect_Field = TypeVar("java_lang_reflect_Field")
Field = java_lang_reflect_Field

T = TypeVar("T")
org_joor_Reflect = TypeVar("org_joor_Reflect")
Reflect = org_joor_Reflect

java_lang_reflect_Method = TypeVar("java_lang_reflect_Method")
Method = java_lang_reflect_Method


class FReflection(PerExecLibrary):
	"""Functions for getting and using raw java classes, methods and functions. 
An instance of this class is passed to scripts as the 'Reflection' variable.\n
	Since: 1.2.3 
	"""
	classLoader: FReflection_CombinedVariableClassLoader

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def getClass(self, name: str) -> Class:
		"""
		Since: 1.2.3 

		Args:
			name: name of class like 'path.to.class' 

		Returns:
			resolved class 
		"""
		pass

	@overload
	def getClass(self, name: str, name2: str) -> Class:
		"""Use this to specify a class with intermediary and yarn names of classes for cleaner code. also has support for
java primitives by using their name in lower case.\n
		Since: 1.2.3 

		Args:
			name: first try 
			name2: second try 

		Returns:
			a Class reference. 
		"""
		pass

	@overload
	def getDeclaredMethod(self, c: Class, name: str, parameterTypes: List[Class]) -> Method:
		"""
		Since: 1.2.3 

		Args:
			c: 
			parameterTypes: 
			name: 
		"""
		pass

	@overload
	def getDeclaredMethod(self, c: Class, name: str, name2: str, parameterTypes: List[Class]) -> Method:
		"""Use this to specify a method with intermediary and yarn names of classes for cleaner code.\n
		Since: 1.2.3 

		Args:
			c: 
			parameterTypes: 
			name: 
			name2: 

		Returns:
			a Method reference. 
		"""
		pass

	@overload
	def getMethod(self, c: Class, name: str, name2: str, parameterTypes: List[Class]) -> Method:
		"""
		Since: 1.6.0 

		Args:
			c: 
			parameterTypes: 
			name: 
			name2: 
		"""
		pass

	@overload
	def getMethod(self, c: Class, name: str, parameterTypes: List[Class]) -> Method:
		"""
		Since: 1.6.0 

		Args:
			c: 
			parameterTypes: 
			name: 
		"""
		pass

	@overload
	def getDeclaredField(self, c: Class, name: str) -> Field:
		"""
		Since: 1.2.3 

		Args:
			c: 
			name: 
		"""
		pass

	@overload
	def getDeclaredField(self, c: Class, name: str, name2: str) -> Field:
		"""Use this to specify a field with intermediary and yarn names of classes for cleaner code.\n
		Since: 1.2.3 

		Args:
			c: 
			name: 
			name2: 

		Returns:
			a Field reference. 
		"""
		pass

	@overload
	def getField(self, c: Class, name: str) -> Field:
		"""
		Since: 1.6.0 

		Args:
			c: 
			name: 
		"""
		pass

	@overload
	def getField(self, c: Class, name: str, name2: str) -> Field:
		"""
		Since: 1.6.0 

		Args:
			c: 
			name: 
			name2: 
		"""
		pass

	@overload
	def invokeMethod(self, m: Method, c: object, objects: List[object]) -> object:
		"""Invoke a method on an object with auto type coercion for numbers.\n
		Since: 1.2.3 

		Args:
			c: object (can be 'null' for statics) 
			objects: 
			m: method 
		"""
		pass

	@overload
	def newInstance(self, c: Class, objects: List[object]) -> T:
		"""Attempts to create a new instance of a class. You probably don't have to use this one and can just call '
new' on a Class unless you're in LUA, but then you also have the (kinda poorly
documented, can someone find a better docs link for me) LuaJava Library .\n
		Since: 1.2.7 

		Args:
			c: 
			objects: 
		"""
		pass

	@overload
	def createClassProxyBuilder(self, clazz: Class, interfaces: List[Class]) -> ProxyBuilder:
		"""proxy for extending java classes in the guest language with proper threading support.\n
		Since: 1.6.0 

		Args:
			interfaces: 
			T: 
			clazz: 
		"""
		pass

	@overload
	def createClassBuilder(self, cName: str, clazz: Class, interfaces: List[Class]) -> ClassBuilder:
		"""
		Since: 1.6.5 

		Args:
			interfaces: 
			T: 
			cName: 
			clazz: 
		"""
		pass

	@overload
	def getClassFromClassBuilderResult(self, cName: str) -> Class:
		"""
		Since: 1.6.5 

		Args:
			cName: 
		"""
		pass

	@overload
	def createLibraryBuilder(self, name: str, perExec: bool, acceptedLangs: List[str]) -> LibraryBuilder:
		pass

	@overload
	def createLibrary(self, className: str, javaCode: str) -> None:
		"""A library class always has a Library annotation containing the name of the library,
which may differ from the actual class name. A library class must also extend BaseLibrary in some way, either directly or through PerExecLibrary , PerExecLanguageLibrary or PerLanguageLibrary .\n
		Since: 1.8.4 

		Args:
			javaCode: the source code of the library 
			className: the fully qualified name of the class, including the package 
		"""
		pass

	@overload
	def compileJavaClass(self, className: str, code: str) -> Class:
		"""A Java Development Kit (JDK) must be installed (and potentially used to start Minecraft) in
order to compile whole classes. 
Compiled classes can't be accessed from any guest language, but must be either stored through FGlobalVars#putObject(java.lang.String,java.lang.Object) or retrieved from this library. Unlike normal
hot swapping, already created instances of the class will not be updated. Thus, it's
important to know which version of the class you're using when instantiating it.\n
		Since: 1.8.4 

		Args:
			code: the java code to compile 
			className: the fully qualified name of the class, including the package 

		Returns:
			the compiled class. 
		"""
		pass

	@overload
	def getCompiledJavaClass(self, className: str) -> Class:
		"""
		Since: 1.8.4 

		Args:
			className: the fully qualified name of the class, including the package 

		Returns:
			the latest compiled class or 'null' if it doesn't exist. 
		"""
		pass

	@overload
	def getAllCompiledJavaClassVersions(self, className: str) -> List[Class]:
		"""
		Since: 1.8.4 

		Args:
			className: the fully qualified name of the class, including the package 

		Returns:
			all compiled versions of the class, in order of compilation. 
		"""
		pass

	@overload
	def getReflect(self, obj: object) -> Reflect:
		"""See jOOR Github for more information.\n
		Since: 1.8.4 

		Args:
			obj: the object to wrap 

		Returns:
			a wrapper for the passed object to do help with java reflection. 
		"""
		pass

	@overload
	def loadJarFile(self, file: str) -> bool:
		"""Loads a jar file to be accessible with this library.\n
		Since: 1.2.6 

		Args:
			file: relative to the script's folder. 

		Returns:
			success value 
		"""
		pass

	@overload
	def loadCurrentMappingHelper(self) -> Mappings:
		"""
		Since: 1.3.1 

		Returns:
			the previous mapping helper generated with FReflection#loadMappingHelper(java.lang.String) 
		"""
		pass

	@overload
	def getClassName(self, o: object) -> str:
		"""
		Since: 1.3.1 

		Args:
			o: class you want the name of 

		Returns:
			the fully qualified class name (with "."'s not "/"'s) 
		"""
		pass

	@overload
	def loadMappingHelper(self, urlorfile: str) -> Mappings:
		"""
		Since: 1.3.1 

		Args:
			urlorfile: a url or file path the the yarn mappings '-v2.jar' file, or '.tiny' file. for example 'https://maven.fabricmc.net/net/fabricmc/yarn/1.16.5%2Bbuild.3/yarn-1.16.5%2Bbuild.3-v2.jar' , if same url/path as previous this will load from cache. 

		Returns:
			the associated mapping helper. 
		"""
		pass

	@overload
	def wrapInstace(self, instance: T) -> WrappedClassInstance:
		"""
		Since: 1.6.5 

		Args:
			instance: 
			T: 
		"""
		pass

	@overload
	def getWrappedClass(self, className: str) -> WrappedClassInstance:
		"""
		Since: 1.6.5 

		Args:
			className: 
		"""
		pass

	pass


