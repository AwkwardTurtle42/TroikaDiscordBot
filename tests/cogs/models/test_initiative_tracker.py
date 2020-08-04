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


def test_display_initiative():
    t = InitiativeTracker()
    t.add_token("Goblin", 2)
    t.add_token("Ogre", 1)
    t.add_token("Henchman", 2)
    t.add_token("Goblin", 2)
    t.add_token("Hero Person", 2)

    assert t.display_tokens() == "Goblin(4) Henchman(2) Hero Person(2) Ogre(1)"


def test_draw_token():
    t = InitiativeTracker()
    t.in_round = True
    t.drawn_log = [[]]
    t.round_bag = ["Goblin", "Ogre", END_OF_ROUND_TOKEN, "Goblin"]
    assert t.count_round_tokens() == 4

    tok = t.draw_token()
    assert tok == "Goblin"
    assert t.in_round
    assert t.count_round_tokens() == 3
    assert t.round_bag == ["Ogre", END_OF_ROUND_TOKEN, "Goblin"]
    assert t.drawn_log == [["Goblin"]]

    tok = t.draw_token()
    assert tok == "Ogre"
    assert t.in_round
    assert t.count_round_tokens() == 2
    assert t.round_bag == [END_OF_ROUND_TOKEN, "Goblin"]
    assert t.drawn_log == [["Goblin", "Ogre"]]

    tok = t.draw_token()
    assert tok == END_OF_ROUND_TOKEN
    assert not t.in_round
    assert t.round_bag == ["Goblin"]
    assert t.drawn_log == [["Goblin", "Ogre", END_OF_ROUND_TOKEN]]

    tok = t.draw_token()
    assert tok == END_OF_ROUND_TOKEN
    assert t.round_bag == ["Goblin"]
    assert t.drawn_log == [["Goblin", "Ogre", END_OF_ROUND_TOKEN]]


def test_start_round_init_tracker():
    t = InitiativeTracker()
    t.add_token("Goblin", 4)
    t.add_token("Vince McFighty", 2)
    t.start_round()
    assert t.in_round
    assert t.count_round_tokens() == 7
    assert t.round_num == 1
    assert t.drawn_log == [[]]

    drawn_tokens = []

    while (True):
        popped = t.draw_token()
        print(popped, t.round_last_drawn)
        drawn_tokens.append(popped)
        if popped == END_OF_ROUND_TOKEN:
            break

    assert drawn_tokens.count("Goblin") + t.round_bag.count("Goblin") == 4
    assert drawn_tokens.count("Vince McFighty") + t.round_bag.count("Vince McFighty") == 2
    assert drawn_tokens[-1] == END_OF_ROUND_TOKEN
    assert t.round_bag.count(END_OF_ROUND_TOKEN) == 0


def test_initiative_shuffles():
    t = InitiativeTracker()
    t.add_token("Goblin", 4)
    t.add_token("Vince McFighty", 2)

    t.start_round()
    turn1 = t.round_bag.copy()

    t.start_round()
    turn2 = t.round_bag.copy()

    assert turn1 != turn2


def test_delay_init_tracker():
    t = InitiativeTracker()
    t.add_token("Goblin", 4)
    t.add_token("Vince McFighty", 2)

    t.start_round()
    assert t.count_round_tokens() == 7
    turn1 = t.round_bag.copy()
    drawn = t.draw_token()
    assert t.count_round_tokens() == 6

    t.delay_token(drawn)
    assert t.count_round_tokens() == 7
    turn1a = t.round_bag.copy()
    assert turn1a != turn1
