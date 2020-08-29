# bot.py
import os
import sys
import logging
import asyncio
import traceback

import discord
from aiohttp import ClientOSError, ClientResponseError
from discord.errors import Forbidden, HTTPException, InvalidArgument, NotFound
from discord.ext import commands
from discord.ext.commands import NoPrivateMessage, ArgumentParsingError, BadArgument
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv

# Stuff to set up the discord bot
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX") or "!"

COGS = (
    "cogs.initiative_cog", "cogs.battle_cog", "cogs.spell_cog", "cogs.luck_cog", "cogs.dice_cog"
)


class TroikaBot(commands.Bot):
    def __init__(self, prefix, description=None, **options):
        super(TroikaBot, self).__init__(prefix, description=description, **options)


desc = '''
TroikaBot, a special bot for playing Troika on discord
'''

bot = TroikaBot(prefix=DISCORD_PREFIX, description=desc, activity=discord.Game(name=f'Troika! | !help'))


# Borrowed from avrae
log_formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
log = logging.getLogger('bot')


# Initialize stuff as the bot comes online.
@bot.event
async def on_ready():
    log.info("Logging in...")


@bot.event
async def on_resumed():
    log.info('resumed.')


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_resumed():
    log.info('resumed.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, (commands.UserInputError, commands.NoPrivateMessage, ValueError)):
        return await ctx.send(
            f"Error: {str(error)}\nUse `{ctx.prefix}help " + ctx.command.qualified_name + "` for help.")

    elif isinstance(error, commands.CheckFailure):
        msg = str(error) or "You are not allowed to run this command."
        return await ctx.send(f"Error: {msg}")

    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send("This command is on cooldown for {:.1f} seconds.".format(error.retry_after))

    elif isinstance(error, commands.MaxConcurrencyReached):
        return await ctx.send(f"Only {error.number} instance{'s' if error.number > 1 else ''} of this command per "
                              f"{error.per.name} can be running at a time.")

    elif isinstance(error, CommandInvokeError):
        original = error.original

        if isinstance(original, Forbidden):
            try:
                return await ctx.author.send(
                    f"Error: I am missing permissions to run this command. "
                    f"Please make sure I have permission to send messages to <#{ctx.channel.id}>."
                )
            except HTTPException:
                try:
                    return await ctx.send(f"Error: I cannot send messages to this user.")
                except HTTPException:
                    return

        elif isinstance(original, NotFound):
            return await ctx.send("Error: I tried to edit or delete a message that no longer exists.")

        elif isinstance(original, (ClientResponseError, InvalidArgument, asyncio.TimeoutError, ClientOSError)):
            return await ctx.send("Error in Discord API. Please try again.")

        elif isinstance(original, HTTPException):
            if original.response.status == 400:
                return await ctx.send(f"Error: Message is too long, malformed, or empty.\n{original.text}")
            elif 499 < original.response.status < 600:
                return await ctx.send("Error: Internal server error on Discord's end. Please try again.")

    await ctx.send(f"Error: {str(error)}")

    log.warning("Error caused by message: `{}`".format(ctx.message.content))
    for line in traceback.format_exception(type(error), error, error.__traceback__):
        log.warning(line)


@bot.event
async def on_command(ctx):
    try:
        log.debug(
            "cmd: chan {0.message.channel} ({0.message.channel.id}), serv {0.message.guild} ({0.message.guild.id}), "
            "auth {0.message.author} ({0.message.author.id}): {0.message.content}".format(
                ctx))
    except AttributeError:
        log.debug("Command in PM with {0.message.author} ({0.message.author.id}): {0.message.content}".format(ctx))


# Register cogs
for cog in COGS:
    bot.load_extension(cog)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
