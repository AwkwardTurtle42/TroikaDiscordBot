import discord.ext.test as dpytest
import pytest

import bot
from cogs.models.weapon import Weapon
from cogs.battle_cog import BattleCog

@pytest.mark.asyncio
async def test_damage_weapon_only(mocker):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(Weapon, "roll_d6", return_value=2)
    cog = BattleCog(tbot)
    tbot.add_cog(cog)

    dpytest.configure(tbot)

    await dpytest.message("!damage Sword")
    dpytest.verify_message("ROLL 1d6 (**2**) -0 [_no armor_] = `2` DAMAGE=`6`")


@pytest.mark.asyncio
@pytest.mark.parametrize("armor,offset,damage", [("light", 1, 6), ("medium", 2, 4), ("heavy", 3, 4), ("no", 0, 6)])
async def test_damage_armor(mocker, armor, offset, damage):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(Weapon, "roll_d6", return_value=3)
    cog = BattleCog(tbot)
    tbot.add_cog(cog)

    dpytest.configure(tbot)

    await dpytest.message(f"!damage Sword {armor}")

    floor_text = ""
    if 3 - offset < 1:
        floor_text = f"= {3-offset} [**min value must be 1**] "

    dpytest.verify_message(f"ROLL 1d6 (**3**) -{offset} [_{armor} armor_] {floor_text}= `{max(3-offset, 1)}` DAMAGE=`{damage}`")


@pytest.mark.asyncio
@pytest.mark.parametrize("armor,offset,damage", [("light", 1, 12), ("medium", 2, 6), ("heavy", 3, 3)])
async def test_damage_ignore_armor(mocker, armor, offset, damage):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(Weapon, "roll_d6", return_value=5)
    tbot.add_cog(BattleCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message(f"!damage Maul {armor}")
    dpytest.verify_message(f"ROLL 1d6 (**5**) -{offset} [_{armor} armor_] +1 [_ignore armor_] = `{5-offset+1}` DAMAGE=`{damage}`")


@pytest.mark.asyncio
async def test_damage_ignore_armor_no_armor(mocker):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(Weapon, "roll_d6", return_value=5)
    tbot.add_cog(BattleCog(bot))

    dpytest.configure(tbot)

    await dpytest.message("!damage Maul")
    dpytest.verify_message("ROLL 1d6 (**5**) -0 [_no armor_] = `5` DAMAGE=`12`")


@pytest.mark.asyncio
async def test_damage_bonus(mocker):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(Weapon, "roll_d6", return_value=3)
    tbot.add_cog(BattleCog(bot))

    dpytest.configure(tbot)

    await dpytest.message("!damage Maul +2")
    dpytest.verify_message("ROLL 1d6 (**3**) -0 [_no armor_] +2 [_damage roll bonus_] = `5` DAMAGE=`12`")


@pytest.mark.asyncio
async def test_attack_outcomes(mocker):
    # FIXME: Test various attack messages using mocks
    pass
