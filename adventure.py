#
# Updates:
#	Refactored main()
#		-added multi-word commands
#		-hopefully made user input airtight
#	Added equipped{} to character class
#	Created Item class
#	Added get() function
#	Added use() function
#		In work
#	Added game_start() function
#

import monster as m
import items as i
import areas as a
import game_functions as gf


# Dictionary for commands and their associated function call
command_list = {

	# Attack commands
	"attack":gf.combat,
	"kill":gf.combat,
	"fight":gf.combat,

	# Inventory command
	"i":gf.inventory,

	# Character sheet command
	"c":gf.char_sheet,

	# Look command
	"l":gf.look,

	# Movement commands
	"n":gf.move,
	"s":gf.move,
	"e":gf.move,
	"w":gf.move,
	"u":gf.move,
	"d":gf.move,
	
	# Get (pick up) commands
	"get":gf.get,
	"grab":gf.get,

	# Use (inventory items) commands
	"use":gf.use,
	
	# Examine command
	"ex":gf.examine,
	
	# Help command
	"help":gf.help_sheet
	
	}

def main():

	# Creates player
	player = gf.game_start()

	# Assigns current area at player start position, then performs look()
	current_area = a.area_list[(player.x_pos, player.y_pos, player.z_pos)]
	gf.look(player, current_area)


	##################
	# Main game loop #
	##################
	while True:
		
		if player.current_hp <= 0:
			print("\n\n-------------------")
			print("G A M E   O V E R !")
			print("-------------------")
			break
		
		command = gf.get_command()
		# Rename list indices for readability	
		command_word = command[0]
		target = command[1]
		target_2 = command[2]
		full_target = target + " " + target_2
		
		# Checks for invalid command input
		# Check for quit input
		if command_word == "quit" or command_word == "exit":
			break
		# Output if too many words are used	
		elif len(command) > 3:
			print("No more than three words at a time, please.")
			continue
		# No input, no output
		elif len(command_word) == 0:
			pass
		# Catch if command does not exist			
		elif command_word not in command_list.keys():
			print(f"{command_word.title()} is not a valid command. "
				f"Type 'help' for help.")
			
		# Valid commands	
		elif command_word in command_list.keys():	
			# If the target is a monster, try to start combat
			if target in m.monster_list.keys() or full_target in m.monster_list.keys():
				try:
					target = m.monster_list[full_target]
					command_list[command_word](player, current_area, target)
				except KeyError:
					target = m.monster_list[target]
					command_list[command_word](player, current_area, target)

			# If the target is an item, try to pick up/use it
			elif target in i.item_list.keys() or full_target in i.item_list.keys():
				try:
					target = i.item_list[full_target]
					command_list[command_word](player, current_area, target)
				except KeyError:
					target = i.item_list[target]
					command_list[command_word](player, current_area, target)
				except TypeError:
					# Function call for item use
					if target in player.inventory_list or full_target in player.inventory_list:
						try:
							target = i.item_list[full_target]
							command_list[command_word](player, target)
						except:
							trget = i.item_list[target]
							command_list[command_word](player, target)

			# If there is no target, try targetless commands
			elif full_target == "__ __":
				try:
					command_list[command_word](player)
				except TypeError:
					try:
						command_list[command_word](player, current_area)
					except TypeError:
						try:
							current_area = command_list[command_word](player, current_area, command_word)
						except:
							print(f"The {command_word} function needs a target.")
			# If command is valid but target is not
			else:
				print(f"The {command_word} command cannot be performed on that.")


if __name__ == "__main__":	
	main()
