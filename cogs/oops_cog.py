import discord
from discord.ext import commands
from cogs.utils import oops

class OopsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Lame but needed for mocks
    def roll_oops(self):
        return oops.roll_oops()

    @commands.command()
    async def oops(self, ctx):
        roll, oops = self.roll_oops()
        await ctx.send(f"d66 (**{roll}**): `{oops}`")


def setup(bot):
    bot.add_cog(OopsCog(bot))
