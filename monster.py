from items import item_list as i


class Monster:
    """Class to define monster and player object attributes"""

    def __init__(self,
                 name="no_name_assigned",
                 max_hp=200,
                 min_dmg=3,
                 max_dmg=10,
                 attack_speed=1.4,
                 exp_value=0,
                 gold_value=0,
                 item=None,
                 drop_chance=0
                 ):

        self.name = name.title()
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.attack_speed = attack_speed
        self.exp_value = exp_value
        self.gold_value = gold_value
        self.item = item
        self.drop_chance = drop_chance

        # Variables only assigned to player; always starts at 0
        self.current_exp = 0
        self.current_gold = 0
        self.inventory_list = [i["health potion"]]
        self.equipped = {
            "head": None,
            "chest": None,
            "hands": None,
            "legs": None,
            "feet": None,
            "finger_1": None,
            "finger_2": None,
            "neck": None,
            "hand_l": None,
            "hand_r": None
        }
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

    def heal(self, heal_value):
        """Method to heal a given amount"""

        if self.current_hp >= self.max_hp:
            print("You are already at maximum health.")
            return False

        # If the difference between current hp and max hp is less than the value that would be healed
        if self.current_hp > self.max_hp - heal_value:
            print(f"You healed for {self.max_hp - self.current_hp}hp.")
            self.current_hp = self.max_hp
            return True

        elif self.current_hp < self.max_hp:
            self.current_hp += heal_value
            print(f"You healed for {heal_value}hp.")
            return True


# Monster class Attributes
#
# name
# max_hp
# min_dmg
# max_dmg
# attack_speed
# exp_value
# gold_value
# item
# drop_chance

monster_list = {
    "weak zombie": Monster(name="Weak Zombie",
                           max_hp=20,
                           min_dmg=0,
                           max_dmg=5,
                           attack_speed=2.4,
                           exp_value=10,
                           gold_value=3,
                           item=i["weak health potion"],
                           drop_chance=30),
    "zombie": Monster(name="Zombie",
                      max_hp=65,
                      min_dmg=3,
                      max_dmg=7,
                      attack_speed=2,
                      exp_value=25,
                      gold_value=11,
                      item=i["weak health potion"],
                      drop_chance=35),
    "strong zombie": Monster(name="Strong Zombie",
                             max_hp=120,
                             min_dmg=6,
                             max_dmg=13,
                             attack_speed=2,
                             exp_value=55,
                             gold_value=18,
                             item=i["health potion"],
                             drop_chance=30)
}
