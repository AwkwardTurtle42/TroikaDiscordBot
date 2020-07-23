# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

# General dice rolling function
# Returns first die, second die, total of both dice
def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2, die1 + die2


# Stuff to set up the discord bot
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

# Initialize the lists used to store the bag and turn log.
bag = ["End The Round"]
total_bag = ["End The Round"]
turn_log = []

# Initialize stuff as the bot comes online.
@bot.event
async def on_ready():
    bag.clear()
    total_bag.clear()
    bag.extend(["End The Round"])
    total_bag.extend(["End The Round"])
    print(f"{bot.user.name} has connected to Discord!")


# Command to empty the bag of all tokens, then return the End The Round token to the bag.
@bot.command(
    name="empty", help="Empties the bag (except End The Round token) and clears log."
)
async def empty(ctx):
    bag.clear()
    total_bag.clear()
    turn_log.clear()
    bag.extend(["End The Round"])
    total_bag.extend(["End The Round"])
    await ctx.send("Bag Emptied")


# Command to add tokens to the bag
# Format: add [number] [token name]
@bot.command(
    name="add", help="Adds [number] [tokens] to the bag. May list more than one pay."
)
async def add(ctx, *args):
    output_string = ""
    for i in range(0, len(args), 2):
        # print(args[i],args[i+1])
        try:
            bag.extend(int(args[i]) * [args[i + 1]])
            total_bag.extend(int(args[i]) * [args[i + 1]])
            output_string += "Added {} {} tokens.\n".format(args[i], args[i + 1])
        except TypeError:
            output_string += "I'm pretty sure '{}' isn't a number.\n".format(args[i])
        except ValueError:
            output_string += "I'm pretty sure '{}' isn't a number.\n".format(args[i])
        except IndexError:
            output_string += (
                "I think you forgot an input, there were an odd number of them.\n"
            )
        except:
            output_string += "What did you do? Something here caused an issue: {} {}\n".format(
                args[i], args[i + 1]
            )
    # bag.extend(number_of_tokens*[name_of_tokens])
    # total_bag.extend(number_of_tokens*[name_of_tokens])
    await ctx.send(output_string)


# Command to remove tokens from the bag
# format: remove [number] [token name]
@bot.command(name="remove", help="Removes [number] [tokens] from the bag.")
async def remove(ctx, number_of_tokens: int, name_of_tokens: str):
    in_bag = total_bag.count(name_of_tokens)
    if in_bag >= number_of_tokens:
        for i in range(number_of_tokens):
            total_bag.remove(name_of_tokens)
        await ctx.send("Removed {} {} tokens.".format(number_of_tokens, name_of_tokens))
    else:
        await ctx.send(
            "Cannot remove {} {} tokens, only {} in bag.".format(
                number_of_tokens, name_of_tokens, in_bag
            )
        )


# command to draw a token from the bag
@bot.command(name="draw", help="Draw a token from the bag.")
async def draw(ctx):
    if len(bag) > 0:
        random.shuffle(bag)
        drawn_token = bag.pop()
        if drawn_token == "End The Round":
            turn_log.extend(["Round End"])
            await ctx.send(
                "**The Round Ends!**\nReturn all tokens to the bag.\nRemove tokens from dead characters and enemies, and resolve any (End of) Round activities.\nThen draw a new token."
            )
        else:
            turn_log.extend([drawn_token])
            await ctx.send(drawn_token)
    else:
        await ctx.send(
            "The bag is empty, nothing to draw! You should probably *return* the tokens to the bag."
        )


# Command to return all drawn tokens to the bag
@bot.command(name="return", help="Return all tokens to the bag.")
async def reset(ctx):
    bag.clear()
    bag.extend(total_bag)
    await ctx.send("All tokens shuffled into bag.")


# Command to display the current contents of the bag, as well as all tokens (including drawn, but not removed tokens)
@bot.command(name="display", help="Displays current and total bag contents.")
async def display_current(ctx):
    bag.sort()
    items = set(total_bag)
    counts = [(total_bag.count(item), bag.count(item)) for item in items]
    item_counts = zip(items, counts)
    output_string = "```{:<20}|{:<10}| {:<10}\n".format("Token", "Total", "Current")
    output_string += "-" * 42
    output_string += "\n"

    for item in item_counts:
        output_string += "{:<20}|{:<10}| {:<10}\n".format(
            item[0], item[1][0], item[1][1]
        )
    output_string += "```"
    await ctx.send(output_string)


# Command to show the turn log
# By default will contain all bag actions
@bot.command(name="log", help="Display initiative log.")
async def log(ctx):
    output_string = ""
    for i, l in enumerate(turn_log):
        output_string += "{}. {}\n".format(i + 1, l)
    await ctx.send(output_string)


# Command to add an entry to the log
# format: entry [log text]
# This lets you put notes for any events you want to keep logged (such as deaths, or changes, or whatever)
@bot.command(name="entry", help="Add an entry to the log.")
async def log(ctx, *entry):
    turn_log.extend([" ".join(entry)])
    await ctx.send("Log entry recorded.")


# Unused commends added during bot testing
# @bot.command(name='test',help='Roll 2d6 and compare against Number')
# async def test(ctx,num):
# 	die1,die2,total = roll_dice()
# 	if total == 12:
# 		result = 'Automatic Failure!'
# 	elif total<=num:
# 		result = 'Success!'
# 	else:
# 		result = 'Failed'
# 	await ctx.send('{} ({},{}) '.format(total,die1,die2) + result)

# @bot.command(name='vstest',help='Roll 2d6 and add a Number')
# async def vstest(ctx,num):
# 	die1,die2,total = roll_dice()

# 	if total == 2:
# 		result = 'Fumble!'
# 	elif total == 12:
# 		result = 'Automatic Failure!'
# 	elif total<=num:
# 		result = 'Success!'
# 	else:
# 		result = 'Failure'

# 	total+=num
# 	await ctx.send('{} ({},{}) '.format(total,die1,die2) + result)

if __name__ == "__main__":
    bot.run(token)
