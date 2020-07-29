import pytest
from cogs.models.initiative_tracker import InitiativeTracker, END_OF_ROUND_TOKEN


def test_init_initiative_tracker():
    t = InitiativeTracker()
    assert t.bag == []


def test_empty_init_tracker():
    t = InitiativeTracker()
    t.add_token("Henchman")
    assert t.count_tokens() == 1
    t.empty()
    assert t.count_tokens() == 0


def test_add_token_init_tracker():
    t = InitiativeTracker()
    assert t.count_tokens() == 0
    t.add_token("Goblin", 4)
    assert t.count_tokens() == 4
    assert t.count_token("Goblin") == 4
    assert t.count_token("Goldfish") == 0


def test_remove_some_tokens_init_tracker():
    t = InitiativeTracker()
    assert t.count_tokens() == 0
    t.add_token("Goblin", 6)
    assert t.count_tokens() == 6
    removed = t.remove_token("Goblin", 4)
    assert removed == 4
    assert t.count_token("Goblin") == 2


def test_remove_all_tokens_init_tracker():
    t = InitiativeTracker()
    assert t.count_tokens() == 0
    t.add_token("Goblin", 4)
    assert t.count_token("Goblin") == 4
    removed = t.remove_token("Goblin", 6)
    assert removed == 4
    assert t.count_token("Goblin") == 0


def test_remove_missing_tokens_init_tracker():
    t = InitiativeTracker()
    assert t.count_tokens() == 0
    t.add_token("Goblin", 4)
    removed = t.remove_token("Ogre", 2)
    assert removed == 0
    assert t.count_token("Goblin") == 4


def test_start_round_init_tracker():
    t = InitiativeTracker()
    t.add_token("Goblin", 4)
    t.add_token("Vince McFighty", 2)
    t.start_round()
    assert t.count_round_tokens() == 7

    returned = {"Goblin": 0, "Vince McFighty": 0, END_OF_ROUND_TOKEN: 0}

    try:
        while (True):
            popped = t.draw_token()
            returned[popped] += 1
    except IndexError:
        pass
    
    assert returned["Goblin"] == 4
    assert returned["Vince McFighty"] == 2
    assert returned[END_OF_ROUND_TOKEN] == 1


def test_initiative_shuffles():
    t = InitiativeTracker()
    t.add_token("Goblin", 4)
    t.add_token("Vince McFighty", 2)

    t.start_round()
    turn1 = t.round_bag.copy()

    t.start_round()
    turn2 = t.round_bag.copy()

    assert turn1 != turn2
