import discord.ext.test as dpytest
import pytest

import bot
from cogs.models.initiative_tracker import InitiativeTracker, END_OF_ROUND_TOKEN
from cogs.initiative_cog import InitiativeCog


@pytest.mark.asyncio
async def test_init_cog_normal(mocker):
    tbot = bot.TroikaBot('!')
    tbot.add_cog(InitiativeCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!i begin")
    dpytest.verify_message("Battle started. Now add tokens with !init add...")

    await dpytest.message("!i add 4 Goblin 6 Ogre 2 Fighter")
    dpytest.verify_message("Added 4 Goblin tokens.\nAdded 6 Ogre tokens.\nAdded 2 Fighter tokens.\n")

    def fixed_shuffle(self):
        self.round_bag = ["Goblin", "Fighter", END_OF_ROUND_TOKEN]

    mocker.patch.object(InitiativeTracker, "shuffle_tokens", new=fixed_shuffle)

    await dpytest.message("!i round")
    dpytest.verify_message("Starting round 1 of combat! Shuffling the bag...")
    dpytest.verify_message("Current Turn: **Goblin**")

    await dpytest.message("!i draw")
    dpytest.verify_message("Current Turn: **Fighter**")

    await dpytest.message("!i current")
    dpytest.verify_message('ROUND 1 current: **Fighter** recent: Goblin')

    await dpytest.message("!i draw")
    dpytest.verify_message("END OF ROUND 1")

    await dpytest.message("!i draw")
    dpytest.verify_message("You are not currently in a round of combat. Start by calling !round")

    await dpytest.message("!i current")
    dpytest.verify_message("You are not currently in a round of combat. Start by calling !round")


@pytest.mark.asyncio
async def test_init_cog_remove_tokens():
    '''Test removing the exact number of tokens of a certain type'''
    tbot = bot.TroikaBot('!')
    tbot.add_cog(InitiativeCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!i begin")
    dpytest.verify_message("Battle started. Now add tokens with !init add...")

    await dpytest.message("!i add 4 Goblin 6 Ogre 2 Troll")
    dpytest.verify_message("Added 4 Goblin tokens.\nAdded 6 Ogre tokens.\nAdded 2 Troll tokens.\n")

    await dpytest.message("!i remove 4 Ogre")
    dpytest.verify_message("Removed 4 out of 6 Ogre tokens in the bag")

    await dpytest.message("!i remove 4 Ogre")
    dpytest.verify_message("You asked to remove 4 Ogre tokens, but there were only 2 left in the bag")

    await dpytest.message("!i remove 4 Goblin")
    dpytest.verify_message("Removed all 4 Goblin tokens from the bag")
