import pytest
from cogs.models.weapon import Weapon
from cogs.models.weapon_list import normalize_weapon_name, normalize_armor_name, WeaponList, ALL_WEAPONS
import mock

def test_normalize_weapon_name():
    '''Test normalizing the weapon name'''
    assert normalize_weapon_name("LonGswORD") == "longsword"
    assert normalize_weapon_name("great  Beast") == "greatbeast"


def test_normalize_armor_name():
    '''Test normalizing the armor name'''
    assert normalize_armor_name("Heavy ArMor") == "heavy"
    assert normalize_armor_name("Medium ArMour") == "medium"
    assert normalize_armor_name("Unarmored") == "unarmored"


def test_weapons_add_weapon():
    w = WeaponList()
    w.add_weapon(Weapon(range(7), name="Angry Squirrel"))
    assert len(w.weapons) == 1
    assert w.weapons['angrysquirrel']


def test_weapons_lookup_weapon_found():
    w = ALL_WEAPONS.lookup_weapon('KnIfE')
    assert w is not None
    assert w.name == 'Knife'
