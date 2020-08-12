import discord.ext.test as dpytest
import bot
import pytest

from cogs.oops_cog import OopsCog


@pytest.mark.asyncio
async def test_oops_cog(mocker):
    tbot = bot.TroikaBot('!')
    oops_cog = OopsCog(tbot)
    tbot.add_cog(oops_cog)

    mocker.patch.object(oops_cog, 'roll_oops', return_value=(23, "A very surprised orc appears."))
    dpytest.configure(tbot)

    await dpytest.message("!oops")
    dpytest.verify_message("d66 (**23**): `A very surprised orc appears.`")
