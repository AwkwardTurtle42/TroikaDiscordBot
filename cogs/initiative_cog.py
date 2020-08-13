import discord
from discord.ext import commands
from discord.ext.commands import NoPrivateMessage

from cogs.models.initiative_tracker import InitiativeTracker, END_OF_ROUND_TOKEN

NOT_IN_ROUND_MESSAGE = "You are not currently in a round of combat. Start by calling !round"

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

    @init.command()
    async def begin(self, ctx, *args):
        """Begins combat in the channel. Users mst add tokens then start rounds"""
        self.init_tracker = InitiativeTracker()
        await ctx.send("Battle started. Now add tokens with !init add...")

    @init.command(name="add", help="Adds [number] [tokens] to the bag. May list more than one player")
    async def add(self, ctx, *args):
        output_string = ""
        for i in range(0, len(args), 2):
            try:
                count = int(args[i])
                token = args[i+1]
                self.init_tracker.add_token(token, count)
                output_string += f"Added {count} {token} tokens.\n"
            except TypeError:
                output_string += "I'm pretty sure '{}' isn't a number.\n".format(args[i])
            except ValueError:
                output_string += "I'm pretty sure '{}' isn't a number.\n".format(args[i])
            except IndexError:
                output_string += (
                    "I think you forgot an input, there were an odd number of them.\n"
                )
            except Exception as e:
                print(e)
                output_string += "What did you do? Something here caused an issue: {} {}\n".format(
                    args[i], args[i + 1]
                )
        await ctx.send(output_string)


    @init.command(name="remove", help="Removes [number] [tokens] from the bag")
    async def remove(self, ctx, count: int, token: str):
        '''Removes N tokens from the bag'''
        in_bag = self.init_tracker.count_token(token)
        removed = self.init_tracker.remove_token(token, count)

        if removed < count:
            await ctx.send(f"You asked to remove {count} {token} tokens, but there were only {removed} left in the bag")
        elif removed < in_bag:
            await ctx.send(f"Removed {removed} out of {in_bag} {token} tokens in the bag")
        else:
            await ctx.send(f"Removed all {removed} {token} tokens from the bag")

    @init.command()
    async def show(self, ctx):
        """Prints out a representation of the tokens in the bag"""
        await ctx.send(f"Initiative Bag: {self.init_tracker.display_tokens()}")
    

    @init.command(name="round", help="Begin a round of combat")
    async def round(self, ctx):
        """Starts a new round and returns the first token"""
        self.init_tracker.start_round()
        await ctx.send(f"Starting round {self.init_tracker.round_num} of combat! Shuffling the bag...")
        await self.draw(ctx)


    @init.command()
    async def draw(self, ctx):
        """Returns a token drawn in the current round"""
        if not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            token = self.init_tracker.draw_token()
            if token == END_OF_ROUND_TOKEN:
                await ctx.send(f"END OF ROUND {self.init_tracker.round_num}")
            else:
                await ctx.send(f"Current Turn: **{token}**")


    @init.command(name="current")
    async def current_turn(self, ctx):
        if not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            token = self.init_tracker.current_token()
            history = self.init_tracker.current_round_history()[:-1]
            history.reverse()
            await ctx.send(f"ROUND {self.init_tracker.round_num} current: **{token}** recent: {', '.join(history)}")


    @init.command(name="delay", help="Puts a token back in the bag and reshuffles it")
    async def delay(self, ctx, token:str):
        if not self.init_tracker.in_round:
            await ctx.send(NOT_IN_ROUND_MESSAGE)
        else:
            self.init_tracker.delay_token(token)
            await ctx.send(f"Pushing {token} back into the initiative tracker")

def setup(bot):
    '''Called by load_extension'''
    bot.add_cog(InitiativeCog(bot))
