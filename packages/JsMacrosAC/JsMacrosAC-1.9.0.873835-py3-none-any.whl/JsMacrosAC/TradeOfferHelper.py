from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .VillagerInventory import VillagerInventory
from .ItemStackHelper import ItemStackHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper

net_minecraft_village_TradeOffer = TypeVar("net_minecraft_village_TradeOffer")
TradeOffer = net_minecraft_village_TradeOffer


class TradeOfferHelper(BaseHelper):

	@overload
	def __init__(self, base: TradeOffer, index: int, inv: VillagerInventory) -> None:
		pass

	@overload
	def getInput(self) -> List[ItemStackHelper]:
		"""

		Returns:
			list of input items required 
		"""
		pass

	@overload
	def getLeftInput(self) -> ItemStackHelper:
		"""The returned item uses the adjusted price, in form of its stack size and will be empty ItemStackHelper#isEmpty() if the first input doesn't exist.\n
		Since: 1.8.4 

		Returns:
			the first input item. 
		"""
		pass

	@overload
	def getRightInput(self) -> ItemStackHelper:
		"""The returned item uses the adjusted price, in form of its stack size and will be empty ItemStackHelper#isEmpty() if the first input doesn't exist.\n
		Since: 1.8.4 

		Returns:
			the second input item. 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""

		Returns:
			output item that will be received 
		"""
		pass

	@overload
	def getIndex(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the index if this trade in the given villager inventory. 
		"""
		pass

	@overload
	def select(self) -> "TradeOfferHelper":
		"""select trade offer on screen
		"""
		pass

	@overload
	def isAvailable(self) -> bool:
		"""
		"""
		pass

	@overload
	def getNBT(self) -> NBTElementHelper_NBTCompoundHelper:
		"""

		Returns:
			trade offer as nbt tag 
		"""
		pass

	@overload
	def getUses(self) -> int:
		"""

		Returns:
			current number of uses 
		"""
		pass

	@overload
	def getMaxUses(self) -> int:
		"""

		Returns:
			max uses before it locks 
		"""
		pass

	@overload
	def shouldRewardPlayerExperience(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if after a successful trade xp will be summoned, 'false' otherwise. 
		"""
		pass

	@overload
	def getExperience(self) -> int:
		"""

		Returns:
			experience gained for trade 
		"""
		pass

	@overload
	def getCurrentPriceAdjustment(self) -> int:
		"""

		Returns:
			current price adjustment, negative is discount. 
		"""
		pass

	@overload
	def getOriginalFirstInput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the original priced item without any adjustments due to rewards or demand. 
		"""
		pass

	@overload
	def getOriginalPrice(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the original price of the item without any adjustments due to rewards or demand. 
		"""
		pass

	@overload
	def getAdjustedPrice(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the adjusted price of the item. 
		"""
		pass

	@overload
	def getSpecialPrice(self) -> int:
		"""A negative value is a discount and means that the player has a good reputation with the
villager, while a positive value is a premium. Hero of the village will always affect and
reduce this value.\n
		Since: 1.8.4 

		Returns:
			the special price multiplier, which affects the price of the item depending on the
player's reputation with the villager. 
		"""
		pass

	@overload
	def getPriceMultiplier(self) -> float:
		"""A higher price multiplier means that the price of these trades can vary much more than normal
ones. The default value is 0.05 and 0.2 for armor and tools.\n
		Since: 1.8.4 

		Returns:
			the price multiplier, which is only depended on the type of trade. 
		"""
		pass

	@overload
	def getDemandBonus(self) -> int:
		"""The demand bonus is globally applied to all trades of this type for all villagers and
players. It is used to increase the price of trades that are in high demand. The demand is
only calculated and updated on restock. Note that a villager can always restock, even if no
items were traded with him. Updating the demand is done with the following formula:  'demand = demand + 2 * uses - maxUses'   
Thus trading only half of the max uses will not increase the demand.
The demand is also capped at 0, so it can not decrease the price.\n
		Since: 1.8.4 

		Returns:
			the demand bonus for this trade. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


