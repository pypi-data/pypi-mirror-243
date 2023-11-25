from typing import overload
from typing import List
from typing import TypeVar

net_minecraft_client_gui_screen_recipebook_RecipeResultCollection = TypeVar("net_minecraft_client_gui_screen_recipebook_RecipeResultCollection")
RecipeResultCollection = net_minecraft_client_gui_screen_recipebook_RecipeResultCollection


class IRecipeBookResults:

	@overload
	def jsmacros_getResultCollections(self) -> List[RecipeResultCollection]:
		pass

	pass


