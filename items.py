class Potion:
    """Class to define health potions"""

    def __init__(self,
                 name,
                 desc,
                 value,
                 alt_names=("potion", "pot"),
                 function="heal"):
        self.name = name.title()
        self.desc = desc
        self.value = value
        self.alt_names = alt_names
        self.function = function
        self.use = True

    @staticmethod
    def heal(target, heal_value):
        """Method to heal a given amount"""

        if target.current_hp >= target.max_hp:
            print("You are already at maximum health.")
            return False

        # If the difference between current hp and max hp is less than the value that would be healed
        if target.current_hp > target.max_hp - heal_value:
            print(f"You healed for {target.max_hp - target.current_hp}hp.")
            target.current_hp = target.max_hp
            return True

        elif target.current_hp < target.max_hp:
            target.current_hp += heal_value
            print(f"You healed for {heal_value}hp.")
            return True


class Equipment:
    """Class to define items to be equipped"""

    def __init__(self,
                 name,
                 desc,
                 alt_names,
                 slot,
                 stats,
                 value,
                 alt_slot=None
                 ):
        self.name = name.title()
        self.desc = desc
        self.alt_names = alt_names
        self.slot = slot
        self.alt_slot = alt_slot
        self.stats = stats
        self.value = value
        self.use = False


# Dictionary for item instances
item_list = {
    # Potions
    "weak health potion": Potion("Weak Health Potion",
                                 desc="Weak Health Potion. Heals the user for 25hp.",
                                 alt_names=("weak", "pot", "potion"),
                                 function="heal",
                                 value=25),
    "health potion": Potion("Health Potion",
                            desc="Health Potion. Heals the user for 40hp.",
                            function="heal",
                            value=40),

    # Gear
    "leather jacket": Equipment("Leather Jacket",
                                desc="It's a Leather Jacket. Why does your wardrobe contain so much leather?\n"
                                     "Raises the wearer's maximum hp by 40.",
                                alt_names=("jacket", "leather"),
                                slot="chest",
                                stats=["max_hp"],
                                value=[40]),
    "leather pants": Equipment("Leather Pants",
                               desc="Leather Pants, just like Eddie Murphy wore.\n"
                                    "Raises the wearer's maximum hp by 35.",
                               alt_names=["pants", "leather"],
                               slot="legs",
                               stats=["max_hp"],
                               value=[35]),
    "leather shoes": Equipment("Leather Shoes",
                               desc="Leather shoes...I mean, couldn't you just call them sneakers?\n"
                                    "Raises the wearer's maximum hp by 10.",
                               alt_names=["shoes", "leather"],
                               slot="feet",
                               stats=["max_hp"],
                               value=[10]),

    # Weapons
    "vibrating sword": Equipment("Vibrating Sword",
                                 desc="A vibrating sword you found in your sister's room. It's wet for some\n"
                                      "reason. She must have been drooling on it in her sleep.\n"
                                      "Raises attack power by 4 and increases attack speed.",
                                 alt_names=["sword", "vibrator"],
                                 slot="main hand",
                                 alt_slot="off hand",
                                 stats=["dmg", "attack_speed"],
                                 value=[4, 1])
}
