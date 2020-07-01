from monster import monster_list as m
from items import item_list as i


class Location:
    """Class to define areas in the game"""

    def __init__(self,
                 description,
                 x_pos,
                 y_pos,
                 z_pos,
                 exits=("n", "s", "e", "w", "u", "d"),
                 monsters=(),
                 items=[]
                 ):

        self.description = description
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.exits = exits
        self.monsters = monsters
        self.items = items


start_area = Location(
    description=f"You awaken ",
    x_pos=0,
    y_pos=0,
    z_pos=0,
    monsters=[m["strong zombie"], m["zombie"]],
    items=[i["health potion"], i["weak health potion"], i["leather jacket"]],
    exits=["n"]
)

tavern_street = Location(
    description=f"You are in a busy street outside of a tavern. "
                f"To the north you can see buildings looming in the distance.",
    x_pos=0,
    y_pos=1,
    z_pos=0,
    monsters=[m["weak zombie"], m["weak zombie"]],
    exits=["s"]
)

area_list = {
    (0, 0, 0): start_area,
    (0, 1, 0): tavern_street
}
