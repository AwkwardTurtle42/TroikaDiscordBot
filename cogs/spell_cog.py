from discord.ext import commands
from cogs.utils import oops, dice

SUCCESS_TOTAL = 2
OOPS_TOTAL = 12


class SpellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Lame but needed for mocks
    def roll_oops(self):
        return oops.roll_oops()

    @commands.command()
    async def spell(self, ctx, skill_points: int):
        roll = dice.roll_under(skill_points)
        if roll.total == SUCCESS_TOTAL:
            await ctx.send("**GUARANTEED SUCCESS** 2d6(1+1)")
        elif roll.total == OOPS_TOTAL:
            await ctx.send("**CATASTROPHIC FAILURE** 2d6(6+6)")
            await self.oops(ctx)
        else:
            await ctx.send(roll.result)

    @commands.command()
    async def oops(self, ctx):
        roll, oops = self.roll_oops()
        await ctx.send(f"OOPS (**{roll}**): `{oops}`")


def setup(bot):
    bot.add_cog(SpellCog(bot))
