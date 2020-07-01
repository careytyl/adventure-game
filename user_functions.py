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
player = m.Monster()
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
                        "do_i", "do_c", "do_l", "do_go", "do_move", "do_help")

    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hidden_methods]

    def precmd(self, line):
        """Overrides default precmd to store user input."""

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

        return True

    do_exit = do_quit

    #####################
    # New Game Function #
    #####################
    @staticmethod
    def new():
        """Starts a new game."""

        # Allows access to global object player
        global player

        player_name = str(input("What is your name? "))

        # Creates generic player with input name
        player = m.Monster(player_name)

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
        if monster == "":
            print("That command requires a target.")
        # If the target is a valid monster, creates an instance of that monster
        elif monster in m.monster_list:
            monster = m.monster_list[monster]
        # If the target is not a valid monster, lets the user know
        else:
            print(f"There is no {arg.title()} here.")

        # If the monster instance is in the current area, begin combat
        if monster in current_area.monsters:

            print(f"You attack a {monster.name}!\n")

            # Combat timer initializations; set to round(Decimal()) because
            # it still wanted to use precision of 28
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
                return True

            elif monster.current_hp <= 0:
                print(f"You have defeated the {monster.name} and gained "
                      f"{monster.exp_value} experience points!\n"
                      f"The {monster.name} has dropped {monster.gold_value} gold!")
                player.current_gold += monster.gold_value
                player.current_exp += monster.exp_value

                # Drop chance if monster has item, then drops into area
                if monster.item is not None:
                    drop = randint(1, 100)
                    if drop < monster.drop_chance:
                        print(f"A {monster.item.name} fell from the monster!")
                        current_area.items.append(monster.item)

                # Removes a defeated monster from the area
                current_area.monsters.remove(monster)

            # Reset monster object hp to max
            monster.current_hp = monster.max_hp

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
            for i in range(0, len(item)):
                print(f"{item[i].name.title()} x{count[i]}")

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
                  f" Attack Speed: {round(1 / player.attack_speed, 2)} per second"
                  )

            print(f"-------------------------------")

    do_c = do_character

    #################
    # Look Function #
    #################
    @staticmethod
    def do_look(arg):
        """Command 'look' or 'l': Allows the user to examine their current surroundings.
        'look <target>' or 'l <target>': Allows the user to examine an item or monster,
            if any additional information is available."""

        if is_empty(arg, "look", req_tgt=False):
            # Prints area description from areas.py
            print(f"{current_area.description}")

            # Displays items in the area, if any
            if len(current_area.items) > 0:
                for ind in range(0, len(current_area.items)):
                    print(f"You spot a {current_area.items[ind].name}!")

            # Displays monsters in the area, if any
            if len(current_area.monsters) > 0:

                # Counts number of unique monsters and stores in dictionary
                monster_count = Counter(current_area.monsters)

                # Creates a list of keys and values for dictionary
                # to allow index reference
                total_count = list(monster_count.values())
                monster = list(monster_count.keys())

                # Iterates through all monster objects in an area and formats output depending on number
                print("You see ", end="")
                for ind in range(0, len(total_count)):

                    # Output when there is more than one of a specific monster
                    if total_count[ind] > 1:
                        print(f"{total_count[ind]} {monster[ind].name}s", end="")

                    if len(total_count) > 2 and ind < len(total_count) - 1:
                        print(", ", end="")

                    elif len(total_count) > 1 and total_count[ind] == total_count[-1]:
                        print(" and ", end="")

                    # Output when there is only a single monster
                    if total_count[ind] == 1:
                        print(f"a {monster[ind].name}", end="")

                print(" here!")

            print(f"Exits: {current_area.exits}")

# *#*#*#*#*#*#*#*#*#*#*#*#* #
# ######################### #
#    Work in progress!      #
# ######################### #
# *#*#*#*#*#*#*#*#*#*#*#*#* #
        elif not is_empty(arg, "look"):
            print("This feature will be implemented soon!")

    do_l = do_look

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

            # Rewrites user input to meet criteria
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
            if direction in current_area.exits:
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
        # "n asdf" from being a valid movement command.
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
            item, counter, item_exists = check_items(arg, location=current_area.items)

            if item is None or counter == 0 and item_exists is False:
                print(f"There are no {arg}s here.")

            # If only one item exists with a given name
            elif counter == 1 or item_exists is True:
                print(f"You picked up the {item.name}.")
                player.inventory_list.append(item)
                current_area.items.remove(item)

            # If there are multiple items with the same alt_name
            elif counter > 1:
                print("Too many similar items. Enter the entire name.")

    ################
    # Use Function #
    ################
    @staticmethod
    def do_use(arg):
        """Command 'use <target>': Uses the targeted item/object from the player's inventory."""

        if not is_empty(arg, "use"):
            # Calls check_items with player inventory as the location to check
            # Sets item, counter, and item_owned variables
            item, counter, item_exists = check_items(arg, location=player.inventory_list)

            if item is None or counter == 0 and item_exists is False:
                print(f"{arg.title()}? You don't have that.")

            elif item.use is False:
                print("You can't use that. Perhaps you can...equip it?")

            elif counter == 1 or item_exists is True:
                if item.function == "heal":
                    item_used = player.heal(item.value)
                    if item_used is True:
                        player.inventory_list.remove(item)

            elif counter > 1:
                print("Too many similar items. Enter the entire name.")

    def do_equip(self, arg):
        """Command 'equip <target>': Equips the target item/object from the player's inventory."""

        item = arg.lower()

        if item == "":
            print("The 'equip' command requires a target.")


def is_empty(arg, command, req_tgt=True):
    """Checks if user input is an empty string."""

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

    for obj in location:

        # Counts the number of times user input appears in items' alt_names
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

    return item, counter, item_exists
