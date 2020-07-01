class Potion:
    """Class to define health potions"""

    def __init__(self,
                 name,
                 value,
                 alt_names=("potion", "pot"),
                 function="heal",
                 use=True):

        self.name = name.title()
        self.value = value
        self.alt_names = alt_names
        self.function = function
        self.use = use


class Equipment:
    """Class to define items to be equipped"""

    def __init__(self,
                 name,
                 alt_names,
                 slot,
                 stat,
                 value,
                 ):

        self.name = name.title()
        self.alt_names = alt_names
        self.slot = slot
        self.stat = stat
        self.value = value
        self.use = False


# Dictionary for item instances

item_list = {
    # Potions
    "weak health potion": Potion("Weak Health Potion",
                                 alt_names=("weak", "pot", "potion"),
                                 function="heal",
                                 value=25),
    "health potion": Potion("Health Potion",
                            function="heal",
                            value=40),

    # Gear
    "leather jacket": Equipment("Leather Jacket",
                                alt_names=("jacket", "leather"),
                                slot="chest",
                                stat="max_hp",
                                value=40)
}
