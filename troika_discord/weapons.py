'''A useful module for computing weapon damage'''
from troika_discord import utils


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
        roll = utils.roll_d6()
        print("Roll ", roll)

        if armor_offset > 0 and self.ignore_armor:
            armor_offset -= 1

        return max(roll - armor_offset + damage_bonus, 1)
