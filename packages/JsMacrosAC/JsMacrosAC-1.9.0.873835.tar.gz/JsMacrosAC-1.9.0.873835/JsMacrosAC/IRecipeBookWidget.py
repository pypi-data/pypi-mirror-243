from typing import overload
from typing import TypeVar

net_minecraft_client_recipebook_ClientRecipeBook = TypeVar("net_minecraft_client_recipebook_ClientRecipeBook")
ClientRecipeBook = net_minecraft_client_recipebook_ClientRecipeBook

net_minecraft_client_gui_screen_recipebook_RecipeBookResults = TypeVar("net_minecraft_client_gui_screen_recipebook_RecipeBookResults")
RecipeBookResults = net_minecraft_client_gui_screen_recipebook_RecipeBookResults


class IRecipeBookWidget:

	@overload
	def jsmacros_getResults(self) -> RecipeBookResults:
		pass

	@overload
	def jsmacros_isSearching(self) -> bool:
		pass

	@overload
	def jsmacros_refreshResultList(self) -> None:
		pass

	@overload
	def jsmacros_getRecipeBook(self) -> ClientRecipeBook:
		pass

	pass


