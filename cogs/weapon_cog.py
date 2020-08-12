import re

import discord
from discord.ext import commands
from discord.ext.commands import NoPrivateMessage, ArgumentParsingError, BadArgument

from cogs.models.weapon import ARMOR_REGEXP_STRING
from cogs.models.weapon_list import ALL_WEAPONS

class WeaponCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['w'], invoke_without_command=True)
    async def weapon(self, ctx):
        await ctx.send(f"Incorrect usage. Use {ctx.prefix}help init for help.")

    # Borrowed this from avrae
    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return True

    @weapon.command(name="damage",
                    brief="Rolls and computes the damage from a weapon against an armor type with an optional bonus. Arguments: weapon [light|medium|heavy] [bonus]",
                    usage="weapon name [light|medium|heavy] [+1]")
    async def damage(self, ctx, *args):
        arg_str = ' '.join(args)

        # DEFINE REGEXPS
        DAMAGE_REGEXP_TWO_INTS = re.compile("(.+) ([+-]?[0-9]+) ([+-]?[0-9]+)")
        DAMAGE_REGEXP_BONUS_ONLY = re.compile("(.+) ([+-]?[0-9]+)")
        DAMAGE_REGEXP_ARMOR_BONUS = re.compile(f"(.+) {ARMOR_REGEXP_STRING} ([+-]?[0-9]+)", flags=re.IGNORECASE)
        DAMAGE_REGEXP_ARMOR = re.compile(f"(.+) ({ARMOR_REGEXP_STRING})", flags=re.IGNORECASE)
        DAMAGE_REGEXP_NONE = re.compile("(.+)")

        # initialize
        regexp_matched = False
        armor = ''
        armor_offset = 0
        bonus = 0

        # weapon, armor offset, bonus offset
        match = DAMAGE_REGEXP_TWO_INTS.match(arg_str)
        if match:
            print("TWO_INTS")
            regexp_matched = True
            weapon_name = match.group(1)
            armor_offset = int(match.group(2))
            bonus = int(match.group(3))

        match = DAMAGE_REGEXP_ARMOR_BONUS.match(arg_str)
        if not regexp_matched and match:
            print("ARMOR_BONUS", match)
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
            bonus = int(match.group(3))

        match = DAMAGE_REGEXP_ARMOR.match(arg_str)
        if not regexp_matched and match:
            print("ARMOR")
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
            bonus = 0

        match = DAMAGE_REGEXP_BONUS_ONLY.match(arg_str)
        if not regexp_matched and match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = "No"
            bonus = int(match.group(2))

        match = DAMAGE_REGEXP_NONE.match(arg_str)
        if not regexp_matched and match:
            print("NONE")
            regexp_matched = True
            weapon_name = match.group(1)
            armor = "No"
            bonus = 0

        if not regexp_matched:
            raise ArgumentParsingError("Unable to parse the inputs. Please check what you wrote.")

        weapon = ALL_WEAPONS.lookup_weapon(weapon_name)
        if weapon is None:
            raise BadArgument(f"Unable to find a weapon definition for `{weapon_name}`. Check your spelling?")

        damage_roll = weapon.roll_damage(armor, bonus)
        damage_amount = weapon.lookup_damage(damage_roll.total)

        await ctx.send(f"ROLL {damage_roll.result} DAMAGE=`{damage_amount}`")


def setup(bot):
    '''Called by extension setup'''
    bot.add_cog(WeaponCog(bot))
