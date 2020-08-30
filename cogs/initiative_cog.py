import re

from discord.ext import commands
from discord.ext.commands import NoPrivateMessage, ArgumentParsingError

from cogs.models.initiative_tracker import InitiativeTracker, END_OF_ROUND_TOKEN

NO_INIT_TRACKER_MESSAGE = "You must start a battle by calling !init start"
NOT_IN_ROUND_MESSAGE = "You are not currently in a round of combat. Start by calling !init round"


class InitiativeCog(commands.Cog):
    """
    Initiative tracking commands. Use !help init for more info.

    """

    def __init__(self, bot):
        self.bot = bot
        self.init_tracker = None

    @commands.group(aliases=['i'], invoke_without_command=True)
    async def init(self, ctx):
        """Commands to help track initiative."""
        await ctx.send(f"Incorrect usage. Use {ctx.prefix}help init for help.")

    # Borrowed this from avrae
    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return True

    @init.command(aliases=["start"])
    async def begin(self, ctx, *args):
        """Begins combat in the channel. Users mst add tokens then start rounds"""
        self.init_tracker = InitiativeTracker()
        if len(args) == 0:
            await ctx.send("Battle started. Now add tokens with !init add...")
        else:
            await ctx.send("Battle started.")
            await ctx.invoke(self.bot.get_command("init add"), arg=' '.join(args))

    @init.command()
    async def end(self, ctx):
        if self.init_tracker is None:
            await ctx.send("It looks like there is no current initiative tracker")
        else:
            await ctx.send("Battle is now ended")
            self.init_tracker = None

    @init.command(name="add", help="Adds [number] [tokens] to the bag. May list more than one player")
    async def add(self, ctx, *, arg):
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
            return

        tokens = re.findall(r'([0-9]+) ([^0-9]+)', arg)
        if tokens == []:
            raise ArgumentParsingError('Argument should be of the form "NUM Token NUM Token"')

        output_string = ""
        for (count, token) in tokens:
            try:
                count = int(count)
                token = token.rstrip()
                self.init_tracker.add_token(token, count)
                output_string += f"Added {count} {token} tokens.\n"
            except Exception as e:
                print(e)
                output_string += "What did you do? Something here caused an issue: {} {}\n".format(
                    args[i], args[i + 1]
                )
        await ctx.send(output_string)

    @init.command(name="remove", help="Removes [number] [tokens] from the bag")
    async def remove(self, ctx, count: int, token: str):
        '''Removes N tokens from the bag'''
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
            return

        in_bag = self.init_tracker.count_token(token)
        removed = self.init_tracker.remove_token(token, count)

        if removed < count:
            await ctx.send(f"You asked to remove {count} {token} tokens, but there were only {removed} left in the bag")
        elif removed < in_bag:
            await ctx.send(f"Removed {removed} out of {in_bag} {token} tokens in the bag")
        else:
            await ctx.send(f"Removed all {removed} {token} tokens from the bag")

    @init.command(name="show", aliases=["bag"])
    async def show(self, ctx):
        """Prints out a representation of the tokens in the bag"""
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
            return

        bag = self.init_tracker.current_tokens()
        output_string = "Initiative Bag:\n"
        for key in sorted(bag):
            output_string += f"- **{key}** ({bag[key]})\n"
        await ctx.send(output_string)

    @init.command(name="round", help="Begin a round of combat")
    async def round(self, ctx):
        """Starts a new round and returns the first token"""
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
            return

        self.init_tracker.start_round()
        await ctx.send(f"Starting round {self.init_tracker.round_num} of combat! Shuffling the bag...")
        await ctx.invoke(self.bot.get_command("init draw"))

    @commands.command(name="round", hidden=True)
    async def roundAlias(self, ctx):
        await ctx.invoke(self.bot.get_command("init round"))
        
    @init.command()
    async def draw(self, ctx):
        """Returns a token drawn in the current round"""
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
        elif not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            token = self.init_tracker.draw_token()
            if token == END_OF_ROUND_TOKEN:
                await ctx.send(f"END OF ROUND {self.init_tracker.round_num}")
            else:
                await ctx.send(f"Current Turn: **{token}**")

    @commands.command(name="draw", hidden=True)
    async def drawAlias(self, ctx):
        await ctx.invoke(self.bot.get_command("init draw"))

    @init.command(name="current")
    async def current_turn(self, ctx):
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
        elif not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            token = self.init_tracker.current_token()
            history = self.init_tracker.current_round_history()[:-1]
            history.reverse()
            await ctx.send(f"ROUND {self.init_tracker.round_num} current: **{token}** recent: {', '.join(history)}")

    @commands.command(name="current", aliases=["turn", "now"], hidden=True)
    async def current_turn_alias(self, ctx):
        await ctx.invoke(self.bot.get_command("init current"))

    @init.command(name="delay", help="Puts a token back in the bag and reshuffles it")
    async def delay(self, ctx, token: str):
        if self.init_tracker is None:
            await ctx.send(NO_INIT_TRACKER_MESSAGE)
        elif not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            self.init_tracker.delay_token(token)
            await ctx.send(f"Pushing {token} back into the initiative tracker")


def setup(bot):
    '''Called by load_extension'''
    bot.add_cog(InitiativeCog(bot))
