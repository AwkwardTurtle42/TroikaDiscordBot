from cogs.utils.dice import roll_d6, roll_2d6, roll_d66

def test_roll_d6():
    for _ in range(100):
        r = roll_d6()
        assert r >= 1 and r <= 6

def test_roll_2d6():
    for _ in range(100):
        r1, r2, r3 = roll_2d6()
        assert r1 >= 1 and r1 <= 6
        assert r2 >= 1 and r2 <= 6
        assert r3 == r1 + r2

def test_roll_d66():
    for _ in range(100):
        r = roll_d66()
        assert r >= 11 and r <= 66

