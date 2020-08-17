import discord.ext.test as dpytest
import bot
import pytest

from cogs.utils import dice
from cogs.spell_cog import SpellCog


@pytest.mark.asyncio
async def test_spell_cog(mocker):
    tbot = bot.TroikaBot('!')
    oops_cog = SpellCog(tbot)
    tbot.add_cog(oops_cog)

    mocker.patch.object(oops_cog, 'roll_oops', return_value=(23, "A very surprised orc appears."))
    dpytest.configure(tbot)

    await dpytest.message("!oops")
    dpytest.verify_message("OOPS (**23**): `A very surprised orc appears.`")

    mocker.patch.object(dice, 'roll_2d6', return_value=(1,2,3))
    await dpytest.message("!spell 7")
    dpytest.verify_message("**SUCCESS** 2d6(1+2) = `3` ≤ `7`")

    mocker.patch.object(dice, 'roll_2d6', return_value=(5,5,10))
    await dpytest.message("!spell 7")
    dpytest.verify_message("**FAILURE** 2d6(5+5) = `10` > `7`")

    mocker.patch.object(dice, "roll_2d6", return_value=(1,1,2))
    await dpytest.message("!spell 1")
    dpytest.verify_message("**GUARANTEED SUCCESS** 2d6(1+1)")

    mocker.patch.object(dice, "roll_2d6", return_value=(6,6,12))
    await dpytest.message("!spell 7")
    dpytest.verify_message("**CATASTROPHIC FAILURE** 2d6(6+6)")
    dpytest.verify_message("OOPS (**23**): `A very surprised orc appears.`")
