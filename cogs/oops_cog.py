import discord
from discord.ext import commands
from cogs.utils.oops import roll_oops

class OopsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def oops(self, ctx):
        roll, oops = roll_oops()
        await ctx.send(f"d66 (**{roll}**): `{oops}`")


def setup(bot):
    bot.add_cog(OopsCog(bot))
