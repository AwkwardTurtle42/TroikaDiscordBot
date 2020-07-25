import pytest
from troika_discord.weapons import *
import mock


def test_normalize_weapon_name():
    '''Test normalizing the weapon name'''
    assert normalize_weapon_name("LonGswORD") == "longsword"
    assert normalize_weapon_name("great  Beast") == "greatbeast"


def test_normalize_armor_name():
    '''Test normalizing the armor name'''
    assert normalize_armor_name("Heavy ArMor") == "heavy"
    assert normalize_armor_name("Unarmored") == "unarmored"


def test_init_exception():
    '''Throwing an exception'''
    with pytest.raises(ValueError):
        Weapon([0, 1, 3])


def test_init_default_values():
    '''Test how it sets optional values by default'''
    weapon = Weapon(range(7))
    assert weapon.damage_table == range(7)
    assert not weapon.two_handed
    assert not weapon.ignore_armor
    assert weapon.name == None
    assert weapon.style == None


def test_init_set_optional_values():
    weapon = Weapon(range(7), name="Vorpal Sword", style="melee", two_handed=True, ignore_armor=True)
    assert weapon.name == "Vorpal Sword"
    assert weapon.style == "melee"
    assert weapon.two_handed
    assert weapon.ignore_armor


def test_basic_damage_roll():
    '''A basic test of damage rolls'''
    with mock.patch('troika_discord.utils.roll_d6', return_value=4):
        w = Weapon(range(7))
        r = w.roll_damage()
        assert r == 4


def test_basic_armor_offset_roll():
    '''Armor offset should reduce damage roll to a minimum of 1'''
    with mock.patch('troika_discord.utils.roll_d6', return_value=2):
        w = Weapon(range(7))
        r = w.roll_damage(armor_offset=2)
        assert r == 1


def test_ignore_armor_offset_roll():
    '''Some weapons ignore one point of the armor offset'''
    with mock.patch('troika_discord.utils.roll_d6', return_value=3):
        w = Weapon(range(7), ignore_armor=True)
        r = w.roll_damage(armor_offset=2)
        assert r == 2 # Ignores one point of armor offset


def test_armor_offset_unarmored_roll():
    '''Ignoring armor should have no effect on unarmored foes'''
    with mock.patch('troika_discord.utils.roll_d6', return_value=2):
        w = Weapon(range(7), ignore_armor=True)
        r = w.roll_damage()
        assert r == 2


def test_attack_damage_mod_roll():
    '''Sometimes there are bonuses on damage rolls'''
    with mock.patch('troika_discord.utils.roll_d6', return_value=2):
        w = Weapon(range(7))
        r = w.roll_damage(damage_bonus=2)
        assert r == 4
