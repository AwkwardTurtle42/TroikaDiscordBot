import bot

def test_roll_dice():
    for _ in range(100):
        r1, r2, r3 = bot.roll_dice()
        assert r1 >= 1 and r1 <= 6
        assert r2 >= 1 and r2 <= 6
        assert r3 == r1 + r2
