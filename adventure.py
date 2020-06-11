import monster as m
import game_functions as gf

# Dictionary for valid command inputs
command_list = {
	"attack":gf.combat,
	"kill":gf.combat,
	"i":gf.inventory,
	"inv":gf.inventory,
	"inventory":gf.inventory,
	"c":gf.char_sheet,
	"char":gf.char_sheet,
	"l":gf.look,
	"look":gf.look,
	"n":gf.move,
	"s":gf.move,
	"e":gf.move,
	"w":gf.move
}


def main():
	
	# Gets player name and creates default player
	player_name = input("What is your name? ")
	
	player = m.Monster(player_name, 200, 200, 3, 10, 1.4, 0, 0)	

	gf.look(player)
	
	# Main game loop
	while True:
		# Accepts player input as a string, then splits into list
		# for command interpretation. Single word commands have
		# None appended to avoid references to invalid indexes
		command = str(input("\n>>> ")).lower()
		command = command.split(" ")
		if len(command) == 1:
			command.append(None)
		
		# Rename list indices for readability	
		command_word = command[0]
		target = command[1]
	
		
		# Check for quit input
		if command_word == "quit":
			break
		
		# Enter combat with target if it is a valid monster
		if target in m.monster_list.keys():
			try:
				command_list[command_word](player, m.monster_list[target])
			except:
				print(f"You cannot use \"{command_word}\" on {target}. "
					f"Try kill {target} or attack {target}.")
					
		elif command_word not in command_list.keys():
			print(f"What does {command_word} mean? Try that command again!\n")
		elif target not in m.monster_list.keys() and target != None:
			print(f"{target.title()} is not a valid target.")
		

			
		
		elif command_word in command_list.keys() and target == None:
			try:
				command_list[command_word](player)
			except:
				command_list[command_word](player, command_word)


if __name__ == "__main__":	
	main()
