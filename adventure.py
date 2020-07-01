# Updates:
# 	- added heal() method to Monster class
# 	- updated inventory display (groups multiple items together)
# 	- updated get() and use() to take partial targets (i.e. pot instead of potion)
# 	- discovered cmd module and replaced all input & functions to work with cmdloop()
# 	- added Equipment class
# 	- added check_items() function and is_empty() function for refactoring purposes
#
# Future updates:
# 	- look() with targets
# 	- Item subclasses
# 		- Consumables
# 		- Equipment
# 	- equip() function
# 	- remove() function
# 	- multiple enemies in combat
# 	- special abilities
# 		- player
# 		- monster
# 	- bosses
# 	- save/load
#
# Known issues:
# 	- get() and use() require full input if more than one of the same item exists

import user_functions as uf


def main():

	# Assigns current area at player start position, then performs look()
	uf.UserInput().new()
	uf.UserInput().do_look(arg="")

	# Begins command loop
	uf.UserInput().cmdloop()

	# Ends game upon loop termination
	print("\n\n-------------------")
	print("G A M E   O V E R !")
	print("-------------------")


if __name__ == "__main__":	
	main()
