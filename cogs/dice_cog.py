import re
from discord.ext import commands
from discord.ext.commands import ArgumentParsingError

from cogs.utils import dice


def modifier_string(modifier):
    if modifier == 0:
        return ""
    elif modifier > 0:
        return f"+{modifier}"
    else:
        return f"{modifier}"


class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll",
                      aliases=["r", "dice"],
                      brief="Roll dice manually",
                      usage="roll d6|d6+4|2d6|d66|d3")
    async def roll(self, ctx, roll_string: str):
        """Rolls the dice"""
        D3_REGEXP = re.compile("d3")
        D6_REGEXP = re.compile("d6([+-][0-9]+)?")
        TWO_D6_REGEXP = re.compile("2d6([+-][0-9]+)?")
        D66_REGEXP = re.compile("d66")

        # initialize
        regexp_matched = False

        match = D66_REGEXP.match(roll_string)
        if match:
            regexp_matched = True
            total = dice.roll_d66()
            await ctx.send(f"d66 = `{total}`")

        match = D3_REGEXP.match(roll_string)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d3()
            await ctx.send(f"d3 ({roll}) = `{roll}`")

        match = D6_REGEXP.match(roll_string)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d6()
            modifier = 0

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(f"d6 ({roll}){modifier_string(modifier)} = `{roll+modifier}`")

        match = TWO_D6_REGEXP.match(roll_string)
        if not regexp_matched and match:
            regexp_matched = True
            r1, r2, total = dice.roll_2d6()
            modifier = 0

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(f"2d6 ({r1}+{r2}){modifier_string(modifier)} = `{total+modifier}`")

        if not regexp_matched:
            raise ArgumentParsingError("Unable to understand your command")

    @commands.command(name="d6", hidden=True)
    async def roll_d6(self, ctx):
        await self.roll(ctx, "d6")

    @commands.command(name="2d6", hidden=True)
    async def roll_2d6(self, ctx):
        await self.roll(ctx, "2d6")


def setup(bot):
    bot.add_cog(DiceCog(bot))
