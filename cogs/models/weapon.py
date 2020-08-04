from cogs.utils import dice

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
    
    def roll_damage(self, armor_offset=0, damage_bonus=0):
        '''Computes a damage roll, adjusting various modifiers'''
        roll = self.roll_d6()
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
