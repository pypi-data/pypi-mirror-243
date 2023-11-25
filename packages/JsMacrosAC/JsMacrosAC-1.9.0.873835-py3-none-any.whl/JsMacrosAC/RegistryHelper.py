from typing import overload
from typing import List
from typing import TypeVar
from .ItemHelper import ItemHelper
from .ItemStackHelper import ItemStackHelper
from .BlockHelper import BlockHelper
from .BlockStateHelper import BlockStateHelper
from .StatusEffectHelper import StatusEffectHelper
from .EnchantmentHelper import EnchantmentHelper
from .EntityHelper import EntityHelper
from .FluidStateHelper import FluidStateHelper

net_minecraft_entity_EntityType__ = TypeVar("net_minecraft_entity_EntityType__")
EntityType = net_minecraft_entity_EntityType__

net_minecraft_util_Identifier = TypeVar("net_minecraft_util_Identifier")
Identifier = net_minecraft_util_Identifier


class RegistryHelper:
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def getItem(self, id: str) -> ItemHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the item's id 

		Returns:
			an ItemHelper for the given item. 
		"""
		pass

	@overload
	def getItemStack(self, id: str) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the item's id 

		Returns:
			an ItemStackHelper for the given item. 
		"""
		pass

	@overload
	def getItemStack(self, id: str, nbt: str) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Args:
			nbt: the item's nbt 
			id: the item's id 

		Returns:
			an ItemStackHelper for the given item and nbt data. 
		"""
		pass

	@overload
	def getItemIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered item ids. 
		"""
		pass

	@overload
	def getItems(self) -> List[ItemHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered items. 
		"""
		pass

	@overload
	def getBlock(self, id: str) -> BlockHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the block's id 

		Returns:
			an BlockHelper for the given block. 
		"""
		pass

	@overload
	def getBlockState(self, id: str) -> BlockStateHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the block's id 

		Returns:
			an BlockStateHelper for the given block. 
		"""
		pass

	@overload
	def getStatusEffect(self, id: str) -> StatusEffectHelper:
		"""

		Args:
			id: the status effect's id 

		Returns:
			an StatusEffectHelper for the given status effect with 0 ticks duration. 
		"""
		pass

	@overload
	def getStatusEffects(self) -> List[StatusEffectHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered status effects as StatusEffectHelper s with 0 ticks duration. 
		"""
		pass

	@overload
	def getBlockState(self, id: str, nbt: str) -> BlockStateHelper:
		"""
		Since: 1.8.4 

		Args:
			nbt: the block's nbt 
			id: the block's id 

		Returns:
			an BlockStateHelper for the given block with the specified nbt. 
		"""
		pass

	@overload
	def getBlockIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered block ids. 
		"""
		pass

	@overload
	def getBlocks(self) -> List[BlockHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered blocks. 
		"""
		pass

	@overload
	def getEnchantment(self, id: str) -> EnchantmentHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the enchantment's id 

		Returns:
			an EnchantmentHelper for the given enchantment. 
		"""
		pass

	@overload
	def getEnchantment(self, id: str, level: int) -> EnchantmentHelper:
		"""
		Since: 1.8.4 

		Args:
			level: the level of the enchantment 
			id: the enchantment's id 

		Returns:
			an EnchantmentHelper for the given enchantment with the specified level. 
		"""
		pass

	@overload
	def getEnchantmentIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered enchantment ids. 
		"""
		pass

	@overload
	def getEnchantments(self) -> List[EnchantmentHelper]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all registered enchantments. 
		"""
		pass

	@overload
	def getEntity(self, type: str) -> EntityHelper:
		"""
		Since: 1.8.4 

		Args:
			type: the id of the entity's type 

		Returns:
			an EntityHelper for the given entity. 
		"""
		pass

	@overload
	def getRawEntityType(self, type: str) -> EntityType:
		"""
		Since: 1.8.4 

		Args:
			type: the id of the entity's type 

		Returns:
			an EntityType for the given entity. 
		"""
		pass

	@overload
	def getEntityTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all entity type ids. 
		"""
		pass

	@overload
	def getFluidState(self, id: str) -> FluidStateHelper:
		"""
		Since: 1.8.4 

		Args:
			id: the fluid's id 

		Returns:
			an FluidStateHelper for the given fluid. 
		"""
		pass

	@overload
	def getFeatureIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all feature ids. 
		"""
		pass

	@overload
	def getStructureFeatureIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all structure feature ids. 
		"""
		pass

	@overload
	def getPaintingIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all painting motive ids. 
		"""
		pass

	@overload
	def getParticleTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all particle type ids. 
		"""
		pass

	@overload
	def getGameEventNames(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all game event names. 
		"""
		pass

	@overload
	def getStatusEffectIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all status effect ids. 
		"""
		pass

	@overload
	def getBlockEntityTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all block entity type ids. 
		"""
		pass

	@overload
	def getScreenHandlerIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all screen handler ids. 
		"""
		pass

	@overload
	def getRecipeTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all recipe type ids. 
		"""
		pass

	@overload
	def getVillagerTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all villager type ids. 
		"""
		pass

	@overload
	def getVillagerProfessionIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all villager profession ids. 
		"""
		pass

	@overload
	def getPointOfInterestTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all point of interest type ids. 
		"""
		pass

	@overload
	def getMemoryModuleTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all memory module type ids. 
		"""
		pass

	@overload
	def getSensorTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all villager sensor type ids. 
		"""
		pass

	@overload
	def getActivityTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all villager activity type ids. 
		"""
		pass

	@overload
	def getStatTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all stat type ids. 
		"""
		pass

	@overload
	def getEntityAttributeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all entity attribute ids. 
		"""
		pass

	@overload
	def getPotionTypeIds(self) -> List[str]:
		"""
		Since: 1.8.4 

		Returns:
			a list of all potion type ids. 
		"""
		pass

	@overload
	def getIdentifier(self, identifier: str) -> Identifier:
		"""
		Since: 1.8.4 

		Args:
			identifier: the String representation of the identifier, with the namespace and path 

		Returns:
			the raw minecraft Identifier. 
		"""
		pass

	@overload
	def parseIdentifier(self, id: str) -> Identifier:
		pass

	@overload
	def parseNameSpace(self, id: str) -> str:
		pass

	pass


