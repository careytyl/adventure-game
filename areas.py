from monster import monster_list as m
from items import item_list as i


class Location:
    """Class to define areas in the game"""

    def __init__(self,
                 description,
                 x_pos,
                 y_pos,
                 z_pos,
                 extra_desc=None,
                 hidden_items=None,
                 monsters=(),
                 walls=(),
                 items=None
                 ):

        if extra_desc is None:
            extra_desc = {}

        if items is None:
            items = []

        if hidden_items is None:
            hidden_items = {}

        self.description = description
        self.extra_desc = extra_desc
        self.hidden_items = hidden_items
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.monsters = monsters
        self.walls = walls
        self.items = items

    def find_hidden_items(self, arg):
        """Function to add previously hidden items to the current area or remove blocked movement directions."""

        try:
            # Checks if dictionary value is a list, then makes sure the correct string is used, then truncates to
            # the last value (n, s, etc)
            if isinstance(self.hidden_items[arg], list):
                if self.hidden_items[arg][0] in ["open_n", "open_s", "open_e", "open_w", "open_u", "open_d"]:
                    unlock_dir = (list((self.hidden_items[arg][0]))[-1])

                    # If the value is in walls, prints a message and removes the wall
                    if unlock_dir in self.walls:
                        print(self.hidden_items[arg][1])
                        self.walls.remove(unlock_dir)

            # If value of hidden_item is an object, create an instance of it in current_area
            # then remove it from hidden_items (to prevent duplication of items)
            elif self.hidden_items[arg] is not None:
                print(f"You find a {self.hidden_items[arg].name}!")
                self.items.append(self.hidden_items[arg])
                self.hidden_items[arg] = None

            # Message if an item existed but was removed
            elif self.hidden_items[arg] is None:
                print("There is no longer anything here.")

        except KeyError:
            pass

# Example location creation. Minimum inputs: description, x_pos, y_pox, z_pos
#
# location name = Location(
#     description=f"Primary description of the area using {ul_bold} and {clear} to highlight objects of "
#                 f"importance (i.e. objects to be targeted with 'look'",
#     extra_desc={"target 1": f"In depth description for an object highlighted in description above",
#                 "target 2": f"Can have as many of these as wanted"},
#     hidden_items={"target 1": i["Item Name"]}, key values must match extra_desc key values or will be ignored
#                   or
#                  {"target 1": ["open_n", "You opened a new path!"]}, used to remove intentionally blocked exits
#     x_pos=x location of player,
#     y_pos=y location of player,
#     z_pos=z location of player,
#     monsters=[m["Monster Name"], m["Monster Name"]],
#     walls=["n", "e"], directions that may normally appear but you don't want them to, i.e. walls or locked doors
#     items=[i["Item Name"]]
# )


# Formatting for underline/bold text & clear (normal) text
ul_bold = "\033[4m\033[1m"
clear = "\033[0m"

your_bedroom = Location(
    description=f"Stretching and looking around, you see a crumpled {ul_bold}note{clear} on the floor near\n"
                f"a pile of discarded clothes. You think about looking at the note by typing \"look note\".",
    extra_desc={"note": f"Scrawled on the paper, in what appears to be blood, is the following message:\n\n"
                        f"\033[38;5;196mREMEMBER TO TYPE HELP\n   TO LEARN HOW TO\n  NAVIGATE THIS GAME{clear}\n\n"
                        f"...whatever that means..."},
    hidden_items={"lever": ["open_w", "You pulled a hidden lever and heard a clicking sound."]},
    x_pos=0,
    y_pos=0,
    z_pos=0,
    walls=["w"],
    items=[i["leather jacket"], i["leather pants"], i["leather shoes"]]
)

secret_room = Location(
    description=f"You have found a hidden area!",
    x_pos=-1,
    y_pos=0,
    z_pos=0,
    items=[i["health potion"]]
)

hallway = Location(
    description=f"You are in the hallway of your home. Behind you, to the south,\n"
                f"is your room; ahead of you is your sisters'. Her {ul_bold}door{clear} is partially\n"
                f"ajar. To the east is the rest of the house.",
    extra_desc={"door": f"You can hear some killer snoring from beyond the door. Your sister is\n"
                        f"either out cold or slowly murdering a large animal."},
    x_pos=0,
    y_pos=1,
    z_pos=0
)

sister_bedroom = Location(
    description=f"You are in your older sister's bedroom. She lays sprawled out on the bed.\n"
                f"She drools slightly between monstrous snores. A {ul_bold}drawer{clear} on her\n"
                f"nightstand is slightly ajar, and you can see inside her {ul_bold}closet{clear}.\n"
                f"A {ul_bold}poster{clear} hangs on her wall.",
    extra_desc={"drawer": "You open the drawer.",
                "closet": "You see neatly arranged shoes, lines of clothes on hangers, and other generic items.",
                "poster": "It has a picture of a kitten hanging from a tree branch with the caption, \"Hang in "
                          "there!\""
                },
    hidden_items={"drawer": i["vibrating sword"]},
    x_pos=0,
    y_pos=2,
    z_pos=0
)

living_room = Location(
    description="You are in the living room of your home.",
    monsters=[m["dara"]],
    x_pos=1,
    y_pos=1,
    z_pos=0
)


area_list = {
    # (x, y, z): x - e/w, y = n/s, z = u/d
    (0, 0, 0): your_bedroom,
    (-1, 0, 0): secret_room,
    (0, 1, 0): hallway,
    (0, 2, 0): sister_bedroom,
    (1, 1, 0): living_room
}
