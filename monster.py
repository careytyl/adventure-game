class Monster:
	"""Class to define monster and player object attributes"""
	
	def __init__(self, name, max_hp, current_hp,
		min_dmg, max_dmg, attack_speed, exp_value,
		gold_value, item=None, drop_chance=0):
		self.name = name.title()
		self.max_hp = max_hp
		self.current_hp = current_hp
		self.min_dmg = min_dmg
		self.max_dmg = max_dmg
		self.attack_speed = attack_speed
		self.exp_value = exp_value
		self.gold_value = gold_value
		self.item = item
		self.drop_chance = drop_chance

		# Variables only assigned to player; always starts at 0
		self.current_exp = 0
		self.current_gold = 0
		self.inventory_list = []
		self.x_pos = 0
		self.y_pos = 0
		

# Dictionary for valid monster targets
#
# name, max_hp, current_hp, min_dmg,
# max_dmg, attack_speed, exp_value, gold_value
# item, drop_chance
monster_list = {
	"slime":Monster("Slime", 20, 20, 0, 5, 3, 10, 2, "health potion", 50),
	"zombie":Monster("Weak Zombie", 80, 80, 3, 10, 2, 25, 7),
	"alex":Monster("Powerful Alex", 2000, 2000, 1000, 1000, 2, 0, 0)
}
