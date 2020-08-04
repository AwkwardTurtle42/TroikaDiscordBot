import re

from cogs.utils.dice import roll_d6
from cogs.models.weapon import Weapon


def normalize_weapon_name(name):
    '''Converts a name to all-lower case and removes spaces'''
    return name.lower().replace(" ", "")


def normalize_armor_name(name):
    '''Converts armot name to lower case and removes " armor" from the back'''
    return name.lower().replace(" armor", "").replace(" armour", "")


class WeaponList:
    '''Represents a collection of weapons for the game'''
    def __init__(self):
        self.weapons = {}

    def add_weapon(self, weapon):
        if weapon.name is None:
            raise ValueError("The weapon must have a name")

        key = normalize_weapon_name(weapon.name)
        self.weapons[key] = weapon

    def lookup_weapon(self, name):
        key = normalize_weapon_name(name)
        return self.weapons.get(key, None)


# define standard weapons
STANDARD_WEAPONS = [
    # Melee weapons
    Weapon([4, 6, 6, 6, 6, 8, 10], name="Sword", style="melee"),
    Weapon([2, 2, 6, 6, 8, 10, 12], name="Axe", style="melee"),
    Weapon([2, 2, 2, 2, 4, 8, 10], name="Knife", style="melee"),
    Weapon([2, 4, 4, 4, 4, 6, 8], name="Staff", style="melee"),
    Weapon([1, 2, 4, 6, 8, 10, 12], name="Hammer", style="melee", ignore_armor=True),
    Weapon([4, 4, 6, 6, 8, 8, 10], name="Spear", style="melee"),
    Weapon([4, 6, 8, 8, 10, 12, 14], name="Longsword", style="melee"),
    Weapon([2, 4, 4, 6, 6, 8, 10], name="Mace", style="melee", ignore_armor=True),
    Weapon([2, 4, 4, 8, 12, 14, 18], name="Polearm", style="melee", ignore_armor=True, two_handed=True),
    Weapon([1, 2, 3, 6, 12, 13, 14], name="Maul", style="melee", ignore_armor=True, two_handed=True),
    Weapon([2, 4, 8, 10, 12, 14, 18], name="Greatsword", style="melee", two_handed=True),
    Weapon([1, 1, 2, 3, 6, 8, 10], name="Club", style="melee"),
    Weapon([1, 1, 1, 2, 2, 3, 4], name="Unarmed", style="melee"),
    Weapon([2, 2, 2, 4, 4, 6, 8], name="Shield", style="melee"),

    # Ranged weapons
    Weapon([2, 4, 4, 6, 12, 18, 24], name="Fusil", style="ranged", ignore_armor=True, two_handed=True),
    Weapon([2, 4, 6, 8, 8, 10, 12], name="Bow", style="ranged", two_handed=True),
    Weapon([4, 4, 6, 8, 8, 8, 10], name="Crossbow", style="ranged", two_handed=True),
    Weapon([2, 2, 4, 4, 6, 12, 16], name="Pistolet", style="ranged", ignore_armor=True),

    # Beastly weapons
    Weapon([2, 2, 3, 3, 4, 5, 6], name="Small Beast", style="beastly"),
    Weapon([4, 6, 6, 8, 8, 10, 12], name="Modest Beast", style="beastly"),
    Weapon([4, 6, 8, 10, 12, 14, 16], name="Large Beast", style="beastly", ignore_armor=True),
    Weapon([4, 8, 12, 12, 16, 18, 24], name="Gigantic Beast", style="beastly", ignore_armor=True),

    # Spells
    Weapon([2, 2, 3, 3, 5, 7, 9], name="Jolt", style="spell", ignore_armor=True),
    Weapon([3, 3, 5, 7, 9, 12, 16], name="Fire Bolt", style="spell"),
    Weapon([6, 8, 12, 16, 18, 24, 36], name="Dragon Fire", style="spell")
]


# Note that even though this is defined as a constant, you could still add new weapons to it
ALL_WEAPONS = WeaponList()
for w in STANDARD_WEAPONS:
    ALL_WEAPONS.add_weapon(w)

ARMOR_OFFSETS= {
    "unarmored": 0,
    "light": 1,
    "lightly": 1,
    "modest": 2,
    "modestly": 2,
    "medium": 2,
    "heavy": 3,
    "heavily": 3
}

ARMOR_REGEXP_STRING = f"({'|'.join(ARMOR_OFFSETS.keys())})( armor|armour|armored|armoured)?"

def lookup_armor_offset(armor):
   '''Returns an int, None for the armor offset and a 0, err if it has issues looking up the armor'''
   if armor.isnumeric():
       return int(armor)
   else:
       try:
           offset = ARMOR_OFFSETS[normalize_armor_name(armor)]
           return offset, None
       except KeyError:
           return 0, f"Unable to look up offset for armor: '{armor}' Check the spelling or provide as an integer"
