import time
import decimal
import cmd
from random import randint
from collections import Counter
import areas as a
import monster as m
import items as i


# Global variable initialization
# Creates generic player; updates on program start
player = m.Player()

# Sets the current area; updates during do_movement()
current_area = a.area_list[(player.x_pos, player.y_pos, player.z_pos)]

# Updates during precmd() -- this is the user's input command string
key_command = ""


class UserInput(cmd.Cmd):
    prompt = "\n>>> "

    # Along with get_names method, hides the following commands from the help menu.
    # Done to prevent an obnoxious number of help topics.
    __hidden_methods = ("do_n", "do_s", "do_e", "do_w", "do_d", "do_u",
                        "do_north", "do_south", "do_east", "do_west", "do_down", "do_up",
                        "do_fight", "do_attack", "do_kill", "do_exit",
                        "do_i", "do_c", "do_l", "do_go", "do_move", "do_help",
                        "do_eq", "do_wear", "do_remove", "do_un", "do_open")

    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hidden_methods]

    def precmd(self, line):
        """Overrides default precmd to store user input."""

        # Makes all user input lowercase for easy comparisons
        line = line.lower()

        # Stores user input into global variable key_command (used primarily for movement)
        global key_command
        key_command = line

        return line

    # Default response if an invalid command is entered
    def default(self, arg):
        print("That is not a valid command. Type \"help\" for help.")

    #################
    # Quit Function #
    #################
    @staticmethod
    def do_quit(arg):
        """Command 'quit' or 'exit': Leaves the game."""

        # Really just added this to remove the weak warning for not using the local variable arg
        if is_empty(arg, "quit", req_tgt=False):
            return True

        else:
            print("Type \"quit\" or \"exit\" to quit.")

    do_exit = do_quit

    ###################
    # Combat Function #
    ###################
    @staticmethod
    def do_combat(arg):
        """Command 'fight <target>' or 'kill <target>' or 'attack <target>': Begins combat with a given target."""

        # Sets decimal precision to 4 digits; avoids issues with
        # floating-point arithmetic, allowing number comparisons
        decimal.getcontext().prec = 4

        monster = arg.lower()

        # Verifies user has input a target
        if not is_empty(arg, "kill/attack/fight"):
            # If the target is a valid monster, creates an instance of that monster
            if monster in m.monster_list:
                monster = m.monster_list[monster]

            # If the monster instance is in the current area, begin combat
            if monster in current_area.monsters:

                print(f"You attack a {monster.name}!\n")

                # Combat timer initializations; set to round(Decimal()) because
                # it still wanted to use precision of 28
                c_time = 0

                # Assigns energy levels to their max values
                p_energy = player.energy
                m_energy = monster.energy

                # Assigns attack speeds
                p_attack_speed = round(decimal.Decimal(player.attack_speed), 1)
                m_attack_speed = round(decimal.Decimal(monster.attack_speed), 1)

                # Main combat loop
                # Program sleeps for .1 second intervals, increments combat time,
                # and performs attacks at specified times based on attack speeds
                while player.current_hp > 0 and monster.current_hp > 0:

                    time.sleep(.1)
                    c_time += decimal.Decimal(.1)
                    p_dmg = randint(player.min_dmg, player.max_dmg)
                    p_energy += .5
                    m_dmg = randint(monster.min_dmg, monster.max_dmg)
                    m_energy += .5

                    # Player attack
                    if c_time % p_attack_speed == 0:
                        print(f"You hit the {monster.name} for {p_dmg} points of damage!\n")
                        monster.current_hp -= p_dmg

                    # Monster attack (red text color format)
                    if c_time % m_attack_speed == 0:

                        print(m_energy)
                        energy_cost = 0

                        # Attempts to use an ability if one is assigned
                        # Energy used is returned from function and subtracted from m_energy
                        if monster.abilities is not None:
                            for ability, ability_chance in monster.abilities.items():
                                if energy_cost == 0 and randint(0, 100) < ability_chance:
                                    energy_cost = ability(monster, player, m_energy)
                                    m_energy -= energy_cost

                        # Cannot perform an ability and regular attack at the same time
                        # Energy cost is only not 0 if an ability is successfully used
                        if energy_cost == 0:
                            print(f"\033[31mThe {monster.name} hits you for {m_dmg} points of damage!\033[0m\n")
                            player.current_hp -= m_dmg

                # End of combat checks/outputs & rewards
                if player.current_hp <= 0:
                    print("You have been slain!")
                    return True

                elif monster.current_hp <= 0:
                    print(f"You have defeated the {monster.name} and gained "
                          f"{monster.exp_value} experience points!\n"
                          f"The {monster.name} has dropped {monster.gold_value} gold!")
                    player.current_gold += monster.gold_value
                    player.current_exp += monster.exp_value

                    # Drop chance if monster has item, then drops into area
                    if monster.item is not None:
                        drop = randint(0, 100)
                        if drop < monster.drop_chance:
                            print(f"A {monster.item.name} fell from the monster!")
                            current_area.items.append(monster.item)

                    # Removes a defeated monster from the area
                    current_area.monsters.remove(monster)

                # Reset monster object hp to max
                monster.current_hp = monster.max_hp

            # If the target is not a valid monster, lets the user know
            else:
                print(f"There is no {arg.title()} here.")

    do_kill = do_combat
    do_attack = do_combat
    do_fight = do_combat

    ######################
    # Inventory Function #
    ######################
    def do_inventory(self, arg):
        """Command 'i': Displays current gold and items held by the player."""

        # Runs default message if more than 'i' is entered
        if arg != "":
            self.default(arg)

        else:
            print(f"-------------------------------\n"
                  f"|          Inventory          |\n"
                  f"-------------------------------\n"
                  f"           Gold: {player.current_gold}\n"
                  )

            if len(player.inventory_list) == 0:
                print(" No items\n")

            # Uses counter to count each unique item
            item_count = Counter(player.inventory_list)
            count = list(item_count.values())
            item = list(item_count.keys())

            # Prints items & quantities
            for ind in range(0, len(item)):
                print(f"{item[ind].name.title()} x{count[ind]}")

            print(f"-------------------------------")

    do_i = do_inventory

    ######################
    # Character Function #
    ######################
    def do_character(self, arg):
        """Command 'c': Displays current information about the player."""

        if arg != "":
            self.default(arg)

        else:
            print(f"-------------------------------\n"
                  f"|          Character          |\n"
                  f"-------------------------------\n"
                  f" Name: {player.name}\n"
                  f" EXP: {player.current_exp}\n"
                  f" HP: {player.current_hp}/{player.max_hp}\n"
                  f" Damage: {player.min_dmg}-{player.max_dmg}\n"
                  f" Attack Speed: {round(1 / player.attack_speed, 2)} per second\n\n"
                  f"Equipment:\n"
                  )

            equip_slot = list(player.equipped.keys())

            # Iterates through each equippable slot in player object, checks if the value is None,
            # then prints the slot name and item name, or empty if the value is None
            for slot in range(0, len(equip_slot)):
                if list(player.equipped.values())[slot] is not None:
                    print(f"{equip_slot[slot].title()}:\t"
                          f"{player.equipped[equip_slot[slot]].name}")
                else:
                    print(f"{equip_slot[slot].title()}:\tEmpty")

            print(f"-------------------------------")

    do_c = do_character

    #################
    # Look Function #
    #################
    def do_look(self, arg):
        """Command 'look' or 'l': Allows the user to examine their current surroundings.
        'look <target>' or 'l <target>': Allows the user to examine an item or monster,
            if any additional information is available."""

        if is_empty(arg, "look", req_tgt=False):
            # Prints area description from areas.py
            print(f"{current_area.description}")

            # Displays items in the area, if any
            if len(current_area.items) > 0:
                for ind in range(0, len(current_area.items)):
                    print(f"\033[94mYou spot a {current_area.items[ind].name}!\033[0m")

            # Displays monsters in the area, if any
            if len(current_area.monsters) > 0:

                # Counts number of unique monsters and stores in dictionary
                monster_count = Counter(current_area.monsters)

                # Creates a list of keys and values for dictionary
                # to allow index reference
                count = list(monster_count.values())
                monster = list(monster_count.keys())

                # Iterates through all monster objects in an area and formats output depending on number
                print("\033[91mYou see", end="")
                for ind in range(0, len(count)):

                    # Output for a single monster
                    if count[ind] == 1:
                        print(f" a {monster[ind].name}", end="")

                    # Output when there is more than one of a unique monster
                    if count[ind] > 1:
                        print(f" {count[ind]} {monster[ind].name}s", end="")

                    # 2 or more unique monsters
                    elif len(count) > 1 and count[ind] == count[-1]:
                        print(" and", end="")

                    # 3 or more unique monsters & not on the last
                    elif len(count) > 2 and ind < len(count) - 1:
                        print(", ", end="")

                print(" here!\033[0m")

            print(f"\033[93mExits: {get_area_exits()}\033[0m")

        ###############################
        # Look Function (with target) #
        ###############################
        elif not is_empty(arg, "look"):

            # Checks if arg is a monster & creates an instance of it,
            # then compares that to the current area
            if arg in m.monster_list.keys():
                monster = m.monster_list[arg]
                if monster in current_area.monsters:
                    print(monster.desc)
                else:
                    print(f"There is no {arg} here.")

            # Extra descriptions if available in an area
            elif arg in current_area.extra_desc.keys()\
                    or arg in current_area.hidden_items.keys():
                try:
                    print(current_area.extra_desc[arg])
                    current_area.find_hidden_items(arg)
                except KeyError:
                    current_area.find_hidden_items(arg)

            # If the player looks at themselves:
            elif arg.title() == player.name\
                    or arg.lower() == "me"\
                    or arg.lower() == "self":
                self.do_character(arg="")

            # Checks if arg is an item in the current area, equipped gear, or player inventory
            else:
                in_inv = check_items(arg, location=player.inventory_list)
                in_area = check_items(arg, location=current_area.items)
                in_gear = check_items(arg, location=player.equipped.values())

                if not in_inv and not in_area and not in_gear:
                    print("There is nothing by that name here.")

    do_l = do_look
    do_open = do_look

    #####################
    # Movement Function #
    #####################
    def do_movement(self, arg):
        """Command 'move <n/s/e/w/u/d>' or 'go <n/s/e/w/u/d>': Moves the player in the designated direction.
        May also be performed by simply typing the direction, i.e. 'n' or 'north'"""

        # Allows access/overwrite of current_area global variable
        global current_area

        # Check that a direction was given
        if not is_empty(arg, "move/go"):

            # Rewrites user input to meet criteria (takes the first letter of the command)
            if arg in ["north", "south", "east", "west", "up", "down"]:
                direction = (list(arg))[0]
            else:
                direction = arg

            directions = {
                "n": 1,
                "s": -1,
                "e": 1,
                "w": -1,
                "u": 1,
                "d": -1,
            }

            # Updates player x/y/z position
            if direction in get_area_exits():
                if direction == "n" or direction == "s":
                    player.y_pos += directions[direction]
                elif direction == "e" or direction == "w":
                    player.x_pos += directions[direction]
                else:
                    player.z_pos += directions[direction]

                # Updates current_area and performs look()
                current_area = a.area_list[(player.x_pos, player.y_pos, player.z_pos)]
                self.do_look(arg="")
            elif direction in directions:
                print(f"You cannot go {direction.title()} here.")
            else:
                print(f"{direction.title()} is not a valid movement option.")

    do_go = do_movement
    do_move = do_movement

    #################################
    # Alternate inputs for movement #
    #################################
    @staticmethod
    def do_n(arg):
        """Basic movement commands."""

        # Takes the global variable key_command as direction (arg is empty string
        # when not using move or go, so the single key character is required
        direction = key_command

        # Verifies only one command is entered. Prevents input such as
        # "n s e w" from being a valid movement command.
        if is_empty(arg, direction, req_tgt=False):
            UserInput().do_movement(direction)
        else:
            print("Are you trying to move?")

    # Sets all single word/character movement commands to the do_n method
    do_north = do_n
    do_s = do_n
    do_south = do_n
    do_e = do_n
    do_east = do_n
    do_w = do_n
    do_west = do_n
    do_u = do_n
    do_up = do_n
    do_d = do_n
    do_down = do_n

    ################
    # Get Function #
    ################
    @staticmethod
    def do_get(arg):
        """Command 'get <target>: Picks up the targeted item/object and puts it in the player's inventory."""

        if not is_empty(arg, "get"):
            # Calls check_items with current area items as the location to check
            check_items(arg, location=current_area.items)

    ################
    # Use Function #
    ################
    @staticmethod
    def do_use(arg):
        """Command 'use <target>': Uses the targeted item/object from the player's inventory."""

        if not is_empty(arg, "use"):
            # Calls check_items with player inventory as the location to check
            check_items(arg, location=player.inventory_list)

    @staticmethod
    def do_equip(arg):
        """Command 'equip <target>' pr 'eq <target>' or 'wear <target>': Equips the target
        item/object from the player's inventory."""

        if not is_empty(arg, "equip"):
            # Calls check_items with player inventory as the location to check
            check_items(arg, player.inventory_list)

    do_wear = do_equip
    do_eq = do_equip

    @staticmethod
    def do_unequip(arg):
        """Command 'unequip <target>' or 'un <target>' or 'remove <target>': Removes the target
        item/object from the player's inventory."""

        if not is_empty(arg, "unequip/remove"):
            # Calls check_items with player as the location to check
            check_items(arg, player.equipped.values())

    do_remove = do_unequip
    do_un = do_unequip


def is_empty(arg, command, req_tgt=True):
    """Checks if user input is an empty string."""

    arg = arg.lower()

    # If the string is empty but requires a target
    if arg == "" and req_tgt is True:
        print(f"The '{command.lower()}' command requires a target.")
        return True

    # If the string is empty but does not require a target
    elif arg == "" and req_tgt is False:
        return True

    # If the string is not empty
    else:
        return False


def check_items(arg, location):
    """Iterates through given location for user input."""

    item_check = arg.lower()
    item_exists = False
    item = None
    counter = 0

    # Stores first input word from command line
    command = key_command.split()[0]

    for obj in location:
        try:
            # Counts the number of times user input appears in items' alt_names
            # Increments counter variable. If more than one, requests more specific input
            if item_check in obj.__getattribute__("alt_names"):
                counter += 1
                item = i.item_list[obj.name.lower()]

            # Checks for full name input, breaks if found
            # item_owned used in the event that full item name input but not first in inventory list
            # (i.e. item is third on list; counter could be > 1)
            elif item_check.title() in obj.__getattribute__("name"):
                item_exists = True
                item = i.item_list[obj.name.lower()]
                break

        except AttributeError:
            pass

    # Returns values when look command is invoked
    # (look requires check_items function to run multiple times)
    # if command == "look" or command == "l":
    #     return item, counter, item_exists

    if item is None or counter == 0 and not item_exists:
        # Look command checks player inventory, area items, and equipped items
        # Return False prevents output message printing multiple times
        if command in ["look", "l"]:
            return False
        else:
            print(f"There are no {arg}s here.")

    # If only one item exists with a given name
    elif counter == 1 or item_exists:

        if command in ["look", "l"]:
            print(f"{item.desc}")
            return True

        # Get function
        if command == "get":

            print(f"You picked up the {item.name}.")
            player.inventory_list.append(item)
            current_area.items.remove(item)

        # Use function
        if command == "use":

            if item.use is False:
                print("You can't use that. Perhaps you can...equip it?")

            elif item.function == "heal":
                item_used = item.heal(player, item.value)
                if item_used is True:
                    player.inventory_list.remove(item)

        # Wear/Equip function
        if command in ["wear", "equip"]:

            if item.use is True:
                print("You can't equip that, dummy. Try using it instead.")

            # Checks that slot is currently empty and equips item if not
            elif player.equipped[item.slot] is None:
                print(f"Equipped {item.name}.")
                player.equipped[item.slot] = item

                # Changes stats based on item.stats & item.value
                for ind in range(0, len(item.stats)):
                    if item.stats[ind] == "max_hp":
                        player.max_hp += item.value[ind]
                        player.current_hp += item.value[ind]

                    if item.stats[ind] == "dmg":
                        player.min_dmg += item.value[ind]
                        player.max_dmg += item.value[ind]

                    if item.stats[ind] == "attack_speed":
                        player.attack_speed -= item.value[ind]

                player.inventory_list.remove(item)

            # If the item has a valid alt_slot (i.e. something that can be held in either hand)
            # and the main slot is already occupied
            elif player.equipped[item.alt_slot] is None:
                print(f"Equipped {item.name}.")
                player.equipped[item.alt_slot] = item

                # Changes stats based on item.stats & item.value
                for ind in range(0, len(item.stats)):
                    if item.stats[ind] == "max_hp":
                        player.max_hp += item.value[ind]
                        player.current_hp += item.value[ind]

                    if item.stats[ind] == "dmg":
                        player.min_dmg += item.value[ind]
                        player.max_dmg += item.value[ind]

                    if item.stats[ind] == "attack_speed":
                        player.attack_speed -= item.value[ind]

                player.inventory_list.remove(item)

            else:
                print(f"You must first remove your {player.equipped[item.slot].name}.")

        if command in ["remove", "unequip", "un"]:

            if item.use is True:
                print("You don't even have that on, dummy. It's not something you can wear. Try using it instead.")

            # Checks that slot is currently in use and removes item
            elif player.equipped[item.slot] is not None:
                print(f"Removed {item.name}.")
                player.equipped[item.slot] = None

                # Changes stats based on item.stats & item.value
                for ind in range(0, len(item.stats)):
                    if item.stats[ind] == "max_hp":
                        player.max_hp -= item.value[ind]
                        player.current_hp -= item.value[ind]

                    if item.stats[ind] == "dmg":
                        player.min_dmg -= item.value[ind]
                        player.max_dmg -= item.value[ind]

                    if item.stats[ind] == "attack_speed":
                        player.attack_speed += item.value[ind]

                player.inventory_list.append(item)

            else:
                print(f"Your {item.slot} slot is empty.")

    # If there are multiple items with the same alt_name
    elif counter > 1:
        print("Too many similar items. Enter the entire name.")


def intro():
    """Introductory exposition"""

    # Allows access to global object player
    global player

    print("\nYou awaken to the incessant buzzing of your alarm clock. The day has finally arrived -- the day\n"
          "of the Super Comic and General Nerd Convention! You hop out of bed, still a bit groggy, and pick\n"
          "up the name tag you've been waiting to use for many months. Lifting a Sharpie® and tapping it \n"
          "thoughtfully against your lip, you contemplate the best way to fill in the blank.\n")

    player_name = str(input("Hi! My name is: "))

    # Creates generic player with input name
    player = m.Player(player_name)


def get_area_exits():
    """Determines valid exits from the current area"""

    exits = []

    if (player.x_pos, player.y_pos + 1, player.z_pos) in a.area_list.keys()\
            and "n" not in current_area.walls:
        exits.append("n")
    if (player.x_pos, player.y_pos - 1, player.z_pos) in a.area_list.keys()\
            and "s" not in current_area.walls:
        exits.append("s")
    if (player.x_pos + 1, player.y_pos, player.z_pos) in a.area_list.keys()\
            and "e" not in current_area.walls:
        exits.append("e")
    if (player.x_pos - 1, player.y_pos, player.z_pos) in a.area_list.keys()\
            and "w" not in current_area.walls:
        exits.append("w")
    if (player.x_pos, player.y_pos, player.z_pos + 1) in a.area_list.keys()\
            and "u" not in current_area.walls:
        exits.append("u")
    if (player.x_pos, player.y_pos, player.z_pos - 1) in a.area_list.keys()\
            and "d" not in current_area.walls:
        exits.append("d")

    return exits
