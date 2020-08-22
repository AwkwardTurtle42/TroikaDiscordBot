from discord.ext import commands
from discord.ext.commands import NoPrivateMessage

from cogs.utils import dice


class LuckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Borrowed this from Avrae
    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return True

    @commands.command(name="luck",
                      aliases=["l"],
                      brief="Tests your luck by rolling 2d6 against your current luck",
                      usages="current_luck")
    async def luck(self, ctx, luck_points: int):
        roll = dice.roll_under(luck_points)
        await ctx.send(roll.result)


def setup(bot):
    bot.add_cog(LuckCog(bot))
