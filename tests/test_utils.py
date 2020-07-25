from troika_discord.utils import *
import mock

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

def test_oops_hit():
    for r1 in range(1, 6):
        for r2 in range(1, 6):
            total = r1*10 + r2
            with mock.patch('troika_discord.utils.roll_d66', return_value=total):
                roll, msg = roll_oops()
                assert roll == total
                assert msg == OOPS_TABLE[total]
