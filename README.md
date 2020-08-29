# Troika Discord Bot
This is a discord bot developed to aid in running the Tabletop RPG Troika! Numinous Edition.
Originally developed by AwkwardTurtle42, with contributions from natehole and harrisj, and some code adapted from [avrae](https://github.com/avrae/avrae)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Supported Commands

### Dice Rolling

|Command|Output|Aliases|
|----|---|-----|
|`!roll d3`|d3 (2) = `2`||
|`!roll d6`|d6 (2) = `2`|`!d6`|
|`!roll d6+2`|d6 (4)+2 = `6`||
|`!roll d6-3`|d6 (3)-3 = `0`||
|`!roll 2d6`|2d6 (1+4) = `5`|`!2d6`|
|`!roll 2d6+2`|2d6 (2+3)+2 = `7`||
|`!roll 2d6-1`|2d6 (4+5)-1 = `8`||
|`!roll d66`|d66 = `23`|`!d66`|

### Luck

Test your luck against a specific luck count

|Command|Output|Aliases|
|----|----|----|
|`!luck 8`|**SUCCESS** 2d6(3+4) = `7` ≤ `8`|`!l 7`

### Spells

Rolls under a spell's skill and computes success or failure. It also handles critical successes and fumbles (rolling an Oops table lookup as well). You can also manually roll against the Oops table if you would prefer.

|Command|Output|Alias|
|-----|----|----|
|`!spell 9`|**SUCCESS** 2d6(1+2) = `3` ≤ `9`||
|`!oops`|OOPS (**23**): `A very surprised orc appears.`||

### Battle Commands

The attack command takes a skill+advanced skill modifier for the attacker and defender and determines the winner of the battle. It automatically handles mighty blows, fumbles and clinches.

The damage command takes an optional armor argument (with values of _no, light, medium, heavy_) and/or an option for a roll modifier (can be positive or negative). It can also take two numeric arguments if you'd prefer to specify the armor offset as a value. In the future, the system might allow you to define new weapons.

|Command|Output|Alias|
|------|------|-----|
|`!attack 5 6`|Attacker: 2d6(2+3) = 5 + 5 = `10` Defender: 2d6(1+1) = 2 + 6 = `8` **ATTACKER WINS** Roll for damage|`!a 5 6`|
|`!attack 1 3`|Attacker: 2d6(**6+6**) = 12 + 1 = `13` Defender: 2d6(6+5) = 11 + 3 = `14` **ATTACKER MIGHTY BLOW** Attacker wins and should score double damage||
|`!attack 5 1`|Attacker: 2d6(**1+1**) = 2 + 5 = `7` Defender: 2d6(1+2) = 3 + 1 = `4` **ATTACKER FUMBLE** Attacker loses and defender adds a +1 bonus to their damage roll||
|`!damage sword`|ROLL 1d6 (**2**) -0 [_no armor_] = `2` DAMAGE=`6`|`!d sword`|
|`!damage sword medium`|ROLL 1d6 (**3**) -2 [_medium armor_] = `1` DAMAGE = `4`|`!d sword medium`|
|`!damage maul heavy`|ROLL 1d6 (**5**) -3 [_heavy armor_] +1 [_ignore armor_] = `3` DAMAGE=`3`||
|`!damage Maul light +2`|ROLL 1d6(**5**) -1 [_light armor_] +1 [_ignore armor_] +2 [_damage roll bonus_] = `5` DAMAGE=`12`||

### Initiative Tracking

Manage initiative and random draws of tokens for each new round.

|Command|Output|Alias|
|---|---|---|
|`!init begin`|Battle started. Now add tokens with !init add...|`!i begin`|
|`!init add 4 Goblin 6 Ogre 2 Fred`|Added 4 Goblin tokens. Added 6 Ogre tokens. Added 2 Fred tokens.|`!i add`|
|`!init round`|Starting round 1 of combat! Shuffling the bag... Current Turn: **Goblin**|`!i round`|
|`!init draw`|Current Turn: **Fred**|`!i draw`|
|`!init current`|ROUND 1 current: **Fred** recent: Goblin||
|`!init draw`|END OF ROUND 1|`!i draw`|
|`!init remove 2 Ogre`|Removed 2 out of 6 Ogre tokens in the bag|`!i remove 2 Ogre`|
|`!init delay Ogre`|Pushing Ogre back into the initiative tracker|`!i delay Ogre`|

## Running Locally

Currently, the TroikaDiscordBot is not designed to run on a shared and hosted
site (one day!) and it currently does not store or load any state between
sessions or if it crashes. To run it, you will need to obtain a Discord Token
for the guild you want it to be part of.

First, clone or download this repo locally. You will need Python 3 on your system to get started, so verify if it's installed (it probably is) and then run these commands to setup the dependencies needed and verify all tests pass:

``` sh
pip install pipenv
pipenv sync
pipenv run pytest
```

Next, follow [these steps to create a Discord app and generate a token](https://www.writebots.com/discord-bot-token/). You don't need to give your bot an icon, but if you wanted to, I'd suggest the [Troika-compatible icon](https://external-preview.redd.it/KdIV_apUhWV-iyIiNuMmMOMU4GUoW4Mn1p7qVH6o590.jpg?auto=webp&s=54708af775118dc2a802974991e35b889b95fa55). Copy the token and save it in a file named `.env` in the root of your clone with the following contents.

``` sh
export DISCORD_TOKEN=<paste the token here>
export DISCORD_PREFIX="!"
```

Then you can start the bot by running

``` sh
pipenv run python bot.py
```

And it should connect to your Discord server. On Discord, you can test the bot by running some commands.
