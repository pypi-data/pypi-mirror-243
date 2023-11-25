from typing import overload
from typing import List
from typing import TypeVar
from .IRecipeBookResults import IRecipeBookResults

net_minecraft_client_gui_screen_recipebook_RecipeResultCollection = TypeVar("net_minecraft_client_gui_screen_recipebook_RecipeResultCollection")
RecipeResultCollection = net_minecraft_client_gui_screen_recipebook_RecipeResultCollection


class MixinRecipeBookResults(IRecipeBookResults):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_getResultCollections(self) -> List[RecipeResultCollection]:
		pass

	pass


