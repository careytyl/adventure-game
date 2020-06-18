class Item:
	"""Class to define item attributes/uses"""

	def __init__(self, name, atk_bonus=0, hp_bonus=0, as_bonus=0, gold_value=0,
		exp_value=0, heal_value=0, use=False, equip=False):
			self.name = name
			self.atk_bonus = atk_bonus
			self.hp_bonus = hp_bonus
			self.as_bonus = as_bonus
			self.gold_value = gold_value
			self.exp_value = exp_value
			self.heal_value = heal_value
			self.use = use
			self.equip = equip

			
item_list = {
	"health potion":Item("Health Potion", use=True, heal_value=40)
	}
