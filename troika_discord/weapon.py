'''A useful module for computing weapon damage'''
from troika_discord import util


def normalize_weapon_name(name):
    '''Converts a name to all-lower case and removes spaces'''
    return name.lower().replace(" ", "")


def normalize_armor_name(name):
    '''Converts armot name to lower case and removes " armor" from the back'''
    return name.lower().replace(" armor", "")


ARMOR_OFFSETS = {
    'light': 1,
    'medium': 2,
    'heavy': 3
}


class Weapon:
    '''Defining the weapons as objects might be overkill, but I'd like to
    support potential future options where DMs can support adding
    new weapons via bot calls'''

    def __init__(self, damage_table, name=None, style=None, two_handed=False, ignore_armor=False):
        '''Defines a single weapon'''

        if len(damage_table) != 7:
            raise ValueError("You must provide a damage table of 7 elements for this weapon")

        self.damage_table = damage_table
        self.name = name
        self.style = style
        self.two_handed = two_handed
        self.ignore_armor = ignore_armor

    def roll_damage(self, armor_offset=0, damage_bonus=0):
        '''Computes a damage roll, adjusting various modifiers'''
        roll = util.roll_d6()
        print("Roll ", roll)

        if armor_offset > 0 and self.ignore_armor:
            armor_offset -= 1

        return max(roll - armor_offset + damage_bonus, 1)

    def lookup_damage(self, roll):
        '''Given a roll result, look up the damage from the weapon'''
        if (roll < 1):
            raise ValueError("The roll must be a positive value")

        if (roll > 7):
            roll = 7

        # rolls range 1-7, arrays range 0-6
        return self.damage_table[roll-1]


class Weapons:
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

all_weapons = Weapons()
for w in STANDARD_WEAPONS:
    all_weapons.add_weapon(w)
