# Updates:
# 	- look() with targets
# 		- Items in area/inventory/equipped, monsters, and objects in area
# 	- equip() function
# 	- remove() function
# 	- get_area_exits() function
# 		- Removes chance of user error in object creation
# 		- Added 'walls' attribute to area objects
# 			- Will allow for 'locked' doors or other puzzle type stuff
# 	- Added hidden items to areas; allows user to find items rather than
# 		just having them lying on the ground all the time
# 	- Color coded exits, monsters, and items for readability
# 	- Color coded combat function to easily differentiate between player and monster attacks
#
# Future updates:
# 	- Shops
# 		- Buy
# 		- Sell
# 	- Item subclasses
# 		- Consumables
# 		- Equipment
# 	- Multiple enemies in combat
# 	- Special abilities
# 		- Player
# 		- Monster
# 	- Bosses
# 	- Save/load
#
# Known issues:
# 	- get() and use() require full input if more than one of the same item exists

import user_functions as uf


def main():

	# Assigns current area at player start position, then performs look()
	uf.intro()
	uf.UserInput().do_look(arg="")
	uf.get_area_exits()

	# Begins command loop
	uf.UserInput().cmdloop()

	# Ends game upon loop termination
	print("\n\n-------------------")
	print("G A M E   O V E R !")
	print("-------------------")


if __name__ == "__main__":	
	main()
