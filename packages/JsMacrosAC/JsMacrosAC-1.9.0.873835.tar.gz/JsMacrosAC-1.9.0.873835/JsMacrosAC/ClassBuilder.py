from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from typing import Generic
from .MethodWrapper import MethodWrapper
from .ClassBuilder_FieldBuilder import ClassBuilder_FieldBuilder
from .ClassBuilder_MethodBuilder import ClassBuilder_MethodBuilder
from .ClassBuilder_ConstructorBuilder import ClassBuilder_ConstructorBuilder
from .ClassBuilder_AnnotationBuilder import ClassBuilder_AnnotationBuilder

T = TypeVar("T")

class ClassBuilder(Generic[T]):
	"""
	Since: 1.6.5 
	"""
	methodWrappers: Mapping[str, MethodWrapper]
	ctClass: CtClass

	@overload
	def __init__(self, name: str, parent: Class, interfaces: List[Class]) -> None:
		pass

	@overload
	def addField(self, fieldType: Class, name: str) -> "ClassBuilder_FieldBuilder":
		pass

	@overload
	def addField(self, code: str) -> "ClassBuilder":
		"""The code must define the full field, including visibility, type, name and an optional value.
Generic types are not supported and must be explicitly cast in the source code when used.
Annotations are also not supported.
Just like in java, classes from the `java.lang` package don't need a fully qualified name.
Examples are:  'private String name;'  'private java.lang.String name;'  'public java.util.List list = new java.util.ArrayList();'  'static int value = 10;'\n
		Since: 1.8.4 

		Args:
			code: the code for the field 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addMethod(self, returnType: Class, name: str, params: List[Class]) -> "ClassBuilder_MethodBuilder":
		pass

	@overload
	def addMethod(self, code: str) -> "ClassBuilder":
		"""The code must define the full method, including visibility, return type, name and parameters.
Generic types are not supported as return values or arguments, neither can varargs be used.
Annotations are also not supported.
Just like in java, classes from the `java.lang` package don't need a fully qualified name.
Examples are:  'public Object id(Object obj) { return obj; }'  'private void print(String text) { System.out.println(text); }'  'private static java.util.Map toMap(Object[] keys, Object[] values) {
     java.util.Map map = new java.util.HashMap();
     for (int i = 0; i < keys.length; i++) {
         map.put(keys[i], values[i]);
     }
     return map;
 }'  'public String toString() {
     System.out.println(super.toString());
     return "Hello World!";
 }'\n
		Since: 1.8.4 

		Args:
			code: the code for the method 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addConstructor(self, params: List[Class]) -> "ClassBuilder_ConstructorBuilder":
		pass

	@overload
	def addConstructor(self, code: str) -> "ClassBuilder":
		"""The code must define the full constructor, including visibility and parameters.
Generic types are not supported as arguments, neither can varargs be used.
Annotations are also not supported.
Just like in java, classes from the `java.lang` package don't need a fully qualified name.
To make sure the class can be easily instantiated, the visibility of the constructor should be public.
Examples are:  'public MyClass() { }'  'public MyClass(String text) { System.out.println(text); }'  'protected MyClass(String text, int number) { super(text, number, ""); }'  'public MyClass(String text, int number, String other) {
     this(text, number);
     this.other = other;
}'\n
		Since: 1.8.4 

		Args:
			code: the code for the constructor 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def addClinit(self) -> "ClassBuilder_ConstructorBuilder":
		pass

	@overload
	def addAnnotation(self, type: Class) -> "ClassBuilder_AnnotationBuilder":
		pass

	@overload
	def finishBuildAndFreeze(self) -> Class:
		pass

	pass


