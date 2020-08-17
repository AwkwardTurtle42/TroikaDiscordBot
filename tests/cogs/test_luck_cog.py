import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.luck_cog import LuckCog


@pytest.mark.asyncio
async def test_luck(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_2d6", return_value=(3, 4, 7))
    tbot.add_cog(LuckCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!luck 8")
    dpytest.verify_message("**SUCCESS** 2d6(3+4) = `7` ≤ `8`")

    await dpytest.message("!luck 6")
    dpytest.verify_message("**FAILURE** 2d6(3+4) = `7` > `6`")
