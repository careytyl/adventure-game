import time, decimal
from random import randint
import areas

# Sets decimal precision to 4 digits; avoids issues with
# floating-point arithmatic, which causes issues with
# number comparisons in combat function
decimal.getcontext().prec = 4

def combat(player, monster):
	"""A function to handle combat between a player and monster"""

	current_area = areas.areas[(player.x_pos, player.y_pos)]	
	if monster in current_area.monsters:
		
		print(f"You attack a {monster.name}!\n")

		# Combat timer initializations; set to round(Decimal()) because
		#  it still wanted to use precision of 28
		c_time = 0
		p_attack_speed = round(decimal.Decimal(player.attack_speed), 1)
		m_attack_speed = round(decimal.Decimal(monster.attack_speed), 1)
	
		# Main combat loop
		# Program sleeps for .1 second intervals, increments combat time,
		# and performs attacks at specified times based on attack speeds
		while player.current_hp > 0 and monster.current_hp > 0:
		
			time.sleep(.1)
			c_time += decimal.Decimal(.1)
			p_dmg = randint(player.min_dmg, player.max_dmg)
			m_dmg = randint(monster.min_dmg, monster.max_dmg)
		
			if c_time % p_attack_speed == 0:
				print(f"You hit the {monster.name} for {p_dmg} points of damage!\n")
				monster.current_hp -= p_dmg
			
			if c_time % m_attack_speed == 0:
				print(f"The {monster.name} hits you for {m_dmg} points of damage!\n")
				player.current_hp -= m_dmg

		# End of combat checks/outputs & rewards
		if player.current_hp <= 0:
			print("You have been slain!")
		
		elif monster.current_hp <= 0:
			print(f"You have defeated the {monster.name} and gained "
				f"{monster.exp_value} experience points!\n"
				f"The {monster.name} has dropped {monster.gold_value} gold!")
			player.current_gold += monster.gold_value
			player.current_exp += monster.exp_value
		
			# Drop chance if monster has item, then drops into area
			if monster.item != None:
				drop = randint(1, 100)
				if drop < monster.drop_chance:
					print(f"A {monster.item} fell from the monster!")
					current_area.items.append(monster.item)
					
			current_area.monsters.remove(monster)
		
		# Reset monster hp to max
		monster.current_hp = monster.max_hp
	
	elif monster not in current_area.monsters:
		print(f"There is no {monster.name} here...")


def inventory(player):
	"""A function to display contents of inventory"""
	
	print(f"-------------------------------\n"
		f"|          Inventory          |\n"
		f"-------------------------------\n"
		f"           Gold: {player.current_gold}"
	)
	
	if len(player.inventory_list) == 0:
		print(" No items\n")
	
	for item in player.inventory_list:
		print(f"{item.title()}\n")
	
	print(f"-------------------------------")
	
	
def char_sheet(player):
	"""A function to display character information"""
	
	print(f"-------------------------------\n"
		f"|          Character          |\n"
		f"-------------------------------\n"
		f" Name: {player.name}\n"
		f" EXP: {player.current_exp}\n"
		f" HP: {player.current_hp}/{player.max_hp}\n"
		f" Damage: {player.min_dmg}-{player.max_dmg}\n"
		f" Attack Speed: {round(1/player.attack_speed,2)} per second"
	)
	
	print(f"-------------------------------")


def look(player):
	"""A function to display information about the current area"""
	
	# Assigns area object to current_area based on player positions
	current_area = areas.areas[(player.x_pos, player.y_pos)]
	
	print(f"{current_area.description}")
	
	# Displays items in the area, if any
	if len(current_area.items) > 0:
		for item in range(0, len(current_area.items)):
			print(f"You spot a {current_area.items[item]}!")
	
	# Displays monsters in the area, if any		
	if len(current_area.monsters) > 0:
		for monster in range(0, len(current_area.monsters)):
			print(f"There is a {current_area.monsters[monster].name} here...")
	
	print(f"Exits: {current_area.exits}")
			
def move(player, direction):
	"""A function to move between areas"""
	
	current_area = areas.areas[(player.x_pos, player.y_pos)]
	directions = {
		"n": 1,
		"s": -1,
		"e": 1,
		"w": -1
		}
	
	if direction in current_area.exits:
		if direction == "n"  or direction == "s":
			player.y_pos += directions[direction]
		else:
			player.x_pos += directions[direction]
		look(player)
	else:
		print(f"You cannot go {direction.title()} here.")
