import re

import discord
from discord.ext import commands
from discord.ext.commands import NoPrivateMessage, ArgumentParsingError, BadArgument

from cogs.utils import dice
from cogs.models.weapon import ARMOR_REGEXP_STRING
from cogs.models.weapon_list import ALL_WEAPONS

MIGHTY_BLOW_ROLL = 12
FUMBLE_ROLL = 2

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

        bonus = 0

        # weapon, armor offset, bonus offset
        match = DAMAGE_REGEXP_TWO_INTS.match(arg_str)
        if match:
            print("TWO_INTS")
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
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


    def roll_2d6(self):
        dice1, dice2, total = dice.roll_2d6()

        dice_string = ''
        if (dice1 == 6 and dice2 == 6) or (dice1 == 1 and dice2 == 1):
            dice_string = f"**{dice1}**, **{dice2}**"
        else:
            dice_string = f"{dice1}, {dice2}"
        
        return dice.RollResult(total, f"2d6 ({dice_string}) = {total}")

    
    @weapon.command(name="attack",
                    brief="Rolls and computes the winner of an attack. Arguments: attack attacker_skill_mod defender_skill_mod",
                    usage="attack attacker_skill_mod defender_skill_mod")
    async def attack(self, ctx, attacker_mod: int, defender_mod: int):
        attack_roll = self.roll_2d6()
        defense_roll = self.roll_d26()

        attack_total = attack_roll.total + attacker_mod
        defense_total = defense_roll.total + defender_mod

        message_output = f"Attacker: {attack_roll.result} + {attacker_mod} = `{attack_total}`\nDefender: {defense_roll.result} + {defender_mod} = `{defense_total}`\n"

        if attack_roll.total == MIGHTY_BLOW_ROLL and defense_roll.total == MIGHTY_BLOW_ROLL:
            await ctx.send(f"{message_output}**SPECTACULAR CLINCH!** Both weapons shatter! (beasts lose 1d6 stamina)")
        elif attack_roll.total == MIGHTY_BLOW_ROLL:
            await ctx.send(f"{message_output}**ATTACKER MIGHTY BLOW!** Attacker wins and should score double damage against attacker")
        elif defense_roll.total == MIGHTY_BLOW_ROLL:
            await ctx.send(f"{message_output}**DEFENDER MIGHTY BLOW!** Defender wins and should score double damage against defender")
        elif attack_roll.total == FUMBLE_ROLL and defense_roll.total == FUMBLE_ROLL:
            await ctx.send(f"{message_output}**DOUBLE FUMBLE!** Both sides roll damage with a +1 bonus")
        elif attack_roll.total == FUMBLE_ROLL:
            await ctx.send(f"{message_output}**ATTACKER FUMBLE!** Attacker loses and defender adds a +1 bonus to their damage roll")
        elif defense_roll.total == FUMBLE_ROLL:
            await ctx.send(f"{message_output}**DEFENDER FUMBLE!** Defender loses and attacker adds a +1 bonus to their damage roll")
        elif attack_total > defense_total:
            await ctx.send(f"{message_output}**ATTACKER WINS** Roll for damage")
        elif defense_total > attack_total:
            await ctx.send(f"{message_output}**DEFENSE_WINS** Roll for damage")
        else:
            await ctx.send(f"{message_output}**TIE** Nobody takes damage")

        
def setup(bot):
    '''Called by extension setup'''
    bot.add_cog(WeaponCog(bot))
