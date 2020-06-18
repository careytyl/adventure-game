import time, decimal
from random import randint
from collections import Counter
import monster as m
import areas as a


def game_start():
	"""Initial player creation"""
	
	# Gets player name and creates default player
	player_name = input("What is your name? ")
	
	player = m.Monster(player_name, 200, 200, 3, 10, 1.4, 0, 0)
	
	return player


def get_command():
	"""Takes player input and returns as a list"""
	
	# Accepts player input as a string, then splits into list
	# for command interpretation. Single word commands have
	# "__" appended to avoid references to invalid indexes
	command = str(input("\n>>> ")).lower()
	command = command.split(" ")
	if len(command) == 1:
		command.append("__")
		command.append("__")
	if len(command) == 2:
		command.append("__")

	return command


def combat(player, current_area, monster):
	"""A function to handle combat between a player and monster"""
	
	# Sets decimal precision to 4 digits; avoids issues with
	# floating-point arithmatic, allowing number comparisons
	decimal.getcontext().prec = 4
	
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
					print(f"A {monster.item.name} fell from the monster!")
					current_area.items.append(monster.item)
					
			# Removes a defeated monster from the area		
			current_area.monsters.remove(monster)
		
		# Reset monster object hp to max
		monster.current_hp = monster.max_hp
	
	elif monster not in current_area.monsters:
		print(f"There is no {monster.name} here...")


def inventory(player):
	"""A function to display contents of inventory"""
	
	print(f"-------------------------------\n"
		f"|          Inventory          |\n"
		f"-------------------------------\n"
		f"           Gold: {player.current_gold}\n"
	)
	
	if len(player.inventory_list) == 0:
		print(" No items\n")
	
	for item in player.inventory_list:
		print(f"{item.name.title()}\n")
	
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


def look(player, current_area):
	"""A function to display information about the current area"""
	
	# Assigns area object to current_area based on player positions
	
	
	print(f"{current_area.description}")
	
	# Displays items in the area, if any
	if len(current_area.items) > 0:
		for i in range(0, len(current_area.items)):
			print(f"You spot a {current_area.items[i].name}!")
	
	# Displays monsters in the area, if any
	if len(current_area.monsters) > 0:
		
		# Counts number of unique monsters and stores in dictionary
		monster_count = Counter(current_area.monsters)
		
		# Creates a list of keys and values for dictionary
		# to allow index reference
		total_count = list(monster_count.values())
		monster = list(monster_count.keys())
		
		print("You see ", end ="")
		for i in range(0, len(total_count)):

			# Output when there is more than one of a specific monster
			if total_count[i] > 1:
				print(f"{total_count[i]} {monster[i].name}s", end="")
				
			if len(total_count) > 2 and i < len(total_count)-1:
				print(", ", end="")
			
			elif len(total_count) > 1 and total_count[i] == total_count[-1]:
				print(" and ", end="")
			
			# Output when there is only a single monster
			if total_count[i] == 1:
				print(f"a {monster[i].name}", end="")
				
		print(" here!")
			
#		for monster in range(0, len(current_area.monsters)):
#			print(f"There is a {current_area.monsters[monster].name} here...")
	
	print(f"Exits: {current_area.exits}")

	
def move(player, current_area, direction):
	"""A function to move between areas"""

	directions = {
		"n": 1,
		"s": -1,
		"e": 1,
		"w": -1,
		"u": 1,
		"d": -1
		}
	
	# Updates player x/y/z position
	if direction in current_area.exits:
		if direction == "n"  or direction == "s":
			player.y_pos += directions[direction]
		elif direction == "e" or direction == "w":
			player.x_pos += directions[direction]
		else:
			player.z_pos += directions[direction]

		# Updates current_area and performs look()
		current_area = a.area_list[(player.x_pos, player.y_pos, player.z_pos)]
		look(player, current_area)
		return current_area
	else:
		print(f"You cannot go {direction.title()} here.")
		return current_area


def get(player, current_area, item):
	"""A function to pick items up"""

	# When no target is supplied, function gets called with "get"
	# as the target. This was the easiest way to throw an error.
	# Also throws out non-item objects being passed.
	if item not in current_area.items:
		print(f"There are no {item.name}s in this area.")
	
	elif item in current_area.items:
		print(f"You picked up the {item.name}.")
		player.inventory_list.append(item)
		current_area.items.remove(item)


def use(player, item):
	"""A function to use items in player inventory"""
	
	# Makes sure the item is in the player's inventory and can be used
	if item not in player.inventory_list or item.use == False:
		print(f"You don't have that.")
	
	elif item in player.inventory_list and item.use == True:
		for k, v in item.__dict__.items():
			if k == "heal_value" and v > 0:
				if player.current_hp == player.max_hp:
					print("You are already at maximum health.")
					player.inventory_list.append(item)
				elif player.current_hp > player.max_hp - v:
					print(f"You healed for {player.max_hp-player.current_hp}hp.")
					player.current_hp = player.max_hp
				elif player.current_hp < player.max_hp:
					player.current_hp += v
					print(f"You healed for {v}hp.")

					
		player.inventory_list.remove(item)


def examine():
	"""A function to get information about an item"""
	

def help_sheet(player):
	"""A function to list commands"""
	
	print(f"-------------------------------\n"
		f"|             Help            |\n"
		f"-------------------------------\n"
		f"\n"
		f"Attack Commands\t\tItem Commands:\n"
		f"kill <target>\t\tget <target>\n"
		f"attack <target>\t\tuse <target>\n"
		f"fight <target>\n"
		f"\n"
		f"Movement Commands:\tMisc Commands:\n"
		f"North:\tn\t\tLook:\tl\n"
		f"South:\ts\t\tCharacter Info: c\n"
		f"East:\te\t\tExamine: e <target>\n"
		f"West:\tw\n"
		f"Up:\tu\n"
		f"Down:\td\n")
