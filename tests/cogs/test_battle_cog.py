import discord.ext.test as dpytest
import pytest

import bot
from cogs.utils import dice
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
@pytest.mark.parametrize("attacker_roll,defender_roll,attacker_skill,defender_skill,expected", [
    ([6, 6, 12], [6, 6, 12], 3, 3, "Attacker: 2d6(**6+6**) = 12 + 3 = `15`\nDefender: 2d6(**6+6**) = 12 + 3 = `15`\n**SPECTACULAR CLINCH!** Both weapons shatter! (beasts lose 1d6 stamina)"),
    ([6, 6, 12], [6, 5, 11], 1, 3, "Attacker: 2d6(**6+6**) = 12 + 1 = `13`\nDefender: 2d6(6+5) = 11 + 3 = `14`\n**ATTACKER MIGHTY BLOW** Attacker wins and should score double damage"),
    ([5, 6, 11], [6, 6, 12], 3, 1, "Attacker: 2d6(5+6) = 11 + 3 = `14`\nDefender: 2d6(**6+6**) = 12 + 1 = `13`\n**DEFENDER MIGHTY BLOW** Defender wins and should score double damage"),
    ([1, 1, 2],  [1, 1, 2],  1, 2, "Attacker: 2d6(**1+1**) = 2 + 1 = `3`\nDefender: 2d6(**1+1**) = 2 + 2 = `4`\n**DOUBLE FUMBLE** Both sides roll damage with a +1 bonus"),
    ([1, 1, 2],  [1, 2, 3],  5, 1, "Attacker: 2d6(**1+1**) = 2 + 5 = `7`\nDefender: 2d6(1+2) = 3 + 1 = `4`\n**ATTACKER FUMBLE** Attacker loses and defender adds a +1 bonus to their damage roll"),
    ([1, 2, 3],  [1, 1, 2],  1, 5, "Attacker: 2d6(1+2) = 3 + 1 = `4`\nDefender: 2d6(**1+1**) = 2 + 5 = `7`\n**DEFENDER FUMBLE** Defender loses and attacker adds a +1 bonus to their damage roll"),
    ([2, 3, 5],  [2, 3, 5],  3, 2, "Attacker: 2d6(2+3) = 5 + 3 = `8`\nDefender: 2d6(2+3) = 5 + 2 = `7`\n**ATTACKER WINS** Roll for damage"),
    ([2, 3, 5],  [2, 3, 5],  2, 3, "Attacker: 2d6(2+3) = 5 + 2 = `7`\nDefender: 2d6(2+3) = 5 + 3 = `8`\n**DEFENDER WINS** Roll for damage"),
    ([2, 3, 5],  [4, 3, 7],  3, 1, "Attacker: 2d6(2+3) = 5 + 3 = `8`\nDefender: 2d6(4+3) = 7 + 1 = `8`\n**TIE** Nobody takes damage")
])
async def test_attack(mocker, attacker_roll, defender_roll, attacker_skill, defender_skill, expected):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(dice, 'roll_2d6', side_effect=[attacker_roll, defender_roll])
    tbot.add_cog(BattleCog(bot))

    dpytest.configure(tbot)

    await dpytest.message(f"!attack {attacker_skill} {defender_skill}")
    dpytest.verify_message(expected)
