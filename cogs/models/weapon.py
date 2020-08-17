from cogs.utils import dice

ARMOR_OFFSETS = {
    "no": 0,
    "none": 0,
    "unarmored": 0,
    "unarmoured": 0,
    "light": 1,
    "moderate": 2,
    "medium": 2,
    "heavy": 3
}

ARMOR_REGEXP_STRING = "(no|none|unarmored|unarmoured|light|moderate|medium|heavy)"


def normalize_armor_name(name):
    '''Converts armot name to lower case and removes " armor" from the back'''
    return name.lower().replace(" armor", "").replace(" armour", "")


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

    def roll_d6(self):
        '''Doing this because Python mocking is dumb'''
        return dice.roll_d6()

    def lookup_armor_offset(self, armor):
        if armor.isnumeric():
            return int(armor)
        else:
            return ARMOR_OFFSETS[normalize_armor_name(armor)]

    def roll_damage(self, armor="No", damage_bonus=0):
        '''Computes a damage roll, adjusting various modifiers'''
        roll = self.roll_d6()
        roll_display = f"1d6 (**{roll}**)"

        armor_offset = self.lookup_armor_offset(armor)
        roll_display += f" -{armor_offset} [_{armor.lower()} armor_]"
        roll -= armor_offset

        if armor_offset > 0 and self.ignore_armor:
            roll_display += " +1 [_ignore armor_]"
            roll += 1

        if damage_bonus > 0:
            roll_display += f" +{damage_bonus} [_damage roll bonus_]"
            roll += damage_bonus

        if roll < 1:
            roll_display += f" = {roll} [**min value must be 1**]"
            roll = 1

        roll_display += f" = `{roll}`"

        return dice.RollResult(roll, roll_display)

    def lookup_damage(self, roll_total):
        '''Given a roll result, look up the damage from the weapon'''
        if (roll_total < 1):
            raise ValueError("The roll must be a positive value")

        if (roll_total > 7):
            roll_total = 7

        # rolls range 1-7, arrays range 0-6
        return self.damage_table[roll_total - 1]
