import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.dice_cog import DiceCog


@pytest.mark.asyncio
async def test_roll_d3(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_d3", return_value=2)
    tbot.add_cog(DiceCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!roll d3")
    dpytest.verify_message("d3 (2) = `2`")


@pytest.mark.asyncio
async def test_roll_d6(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_d6", return_value=4)
    tbot.add_cog(DiceCog(tbot))
    
    dpytest.configure(tbot)

    await dpytest.message("!roll d6")
    dpytest.verify_message("d6 (4) = `4`")

    await dpytest.message("!d6")
    dpytest.verify_message("d6 (4) = `4`")

    await dpytest.message("!roll d6+2")
    dpytest.verify_message("d6 (4)+2 = `6`")

    await dpytest.message("!roll d6-3")
    dpytest.verify_message("d6 (4)-3 = `1`")


@pytest.mark.asyncio
async def test_roll_2d6(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_2d6", return_value=(1, 4, 5))
    tbot.add_cog(DiceCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!roll 2d6")
    dpytest.verify_message("2d6 (1+4) = `5`")

    await dpytest.message("!2d6")
    dpytest.verify_message("2d6 (1+4) = `5`")

    await dpytest.message("!roll 2d6+3")
    dpytest.verify_message("2d6 (1+4)+3 = `8`")

    await dpytest.message("!roll 2d6-2")
    dpytest.verify_message("2d6 (1+4)-2 = `3`")


@pytest.mark.asyncio
async def test_roll_d66(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_d66", return_value=23)
    tbot.add_cog(DiceCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!roll d66")
    dpytest.verify_message("d66 = `23`")
