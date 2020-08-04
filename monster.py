from items import item_list as i
from random import randint


class Player:
    """Class to define monster and player object attributes"""

    def __init__(self, name="no_name_assigned"):
        self.name = name.title()
        self.max_hp = 250
        self.current_hp = self.max_hp
        self.energy = 50
        self.min_dmg = 1
        self.max_dmg = 3
        self.attack_speed = 2.5
        self.current_exp = 0
        self.current_gold = 0
        self.inventory_list = [i["health potion"]]
        self.equipped = {
            "main hand": None,
            "off hand": None,
            "head": None,
            "chest": None,
            "hands": None,
            "legs": None,
            "feet": None,
            "finger": None,
            "neck": None,
        }
        self.abilities = {},
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0


class Monster:

    def __init__(self,
                 name,
                 desc,
                 max_hp,
                 energy,
                 min_dmg,
                 max_dmg,
                 attack_speed,
                 abilities=None,
                 exp_value=0,
                 gold_value=0,
                 item=None,
                 drop_chance=0):

        self.name = name
        self.desc = desc
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.energy = energy
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.attack_speed = attack_speed
        self.abilities = abilities
        self.exp_value = exp_value
        self.gold_value = gold_value
        self.item = item
        self.drop_chance = drop_chance

    def smash(self, player, energy):
        """Deals max damage + 5"""

        # Required amount of energy passed to function
        energy_cost = 20

        # Checks for enough energy
        if energy >= energy_cost:
            smash_dmg = self.max_dmg + 5

            print(f"\033[31mThe {self.name} smashes you for {smash_dmg} damage!\033[0m")
            player.current_hp -= smash_dmg

            # Returns the cost of the ability to be subtracted
            return energy_cost

        else:
            # Energy cost is 0 if the ability is not used
            return 0

    def dara_spank(self, player, energy):
        """Just humiliates the player a little"""

        # See top-most function (smash) for typical ability function setup
        energy_cost = 10

        if energy >= energy_cost:
            print(f"\033[31m{self.name} bends you over and spanks you for 1 damage!\033[0m")
            player.current_hp -= 1
            return energy_cost

        else:
            return 0


# Monster class Attributes
#
# name
# max_hp
# min_dmg
# max_dmg
# attack_speed
# ability (default none)
# ability chance (default 0)
# exp_value (default 0)
# gold_value (default 0)
# item (default none)
# drop_chance (default 0)

monster_list = {
    "weak zombie": Monster(name="Weak Zombie",
                           desc="This zombie looks particularly weak. Its jaw dangles uselessly, and you wonder"
                                "if it could even bite you.",
                           max_hp=20,
                           energy=25,
                           min_dmg=0,
                           max_dmg=5,
                           attack_speed=2.4,
                           exp_value=10,
                           gold_value=3,
                           item=i["weak health potion"],
                           drop_chance=30),
    "zombie": Monster(name="Zombie",
                      desc="This zombie seems to still have all of its parts. Its lethargic movement gives you"
                           "the sense that it would be fairly easy to dispatch.",
                      max_hp=65,
                      energy=40,
                      min_dmg=3,
                      max_dmg=7,
                      attack_speed=2,
                      exp_value=25,
                      gold_value=11,
                      item=i["weak health potion"],
                      drop_chance=35),
    "dara": Monster(name="Dara",
                    desc="Woah, that is one angry mama!",
                    max_hp=50,
                    energy=20,
                    min_dmg=2,
                    max_dmg=4,
                    attack_speed=.8,
                    abilities={Monster.smash: 25,
                               Monster.dara_spank: 50},
                    exp_value=1000,
                    gold_value=1000,
                    item=i["vibrating sword"],
                    drop_chance=100)
}
