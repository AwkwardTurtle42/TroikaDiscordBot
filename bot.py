# bot.py
import os
import sys
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Stuff to set up the discord bot
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

COGS = (
    "cogs.initiative_cog", "cogs.battle_cog", "cogs.spell_cog", "cogs.luck_cog", "cogs.dice_cog"
)


class TroikaBot(commands.Bot):
    def __init__(self, prefix, description=None, **options):
        super(TroikaBot, self).__init__(prefix, description=description, **options)


desc = '''
TroikaBot, a special bot for playing Troika on discord
'''

bot = TroikaBot(prefix='!', description=desc, activity=discord.Game(name=f'Troika! | !help'))


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
