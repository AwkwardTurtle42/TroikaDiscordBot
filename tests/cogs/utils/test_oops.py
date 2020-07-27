import mock
from cogs.utils.oops import roll_oops, OOPS_TABLE

def test_oops_table():
    '''Runs through every value in the oops table'''
    for r1 in range(1, 6):
        for r2 in range(1, 6):
            total = r1*10 + r2
            with mock.patch(f'{roll_oops.__module__}.roll_d66', return_value=total):
                roll, msg = roll_oops()
                assert roll == total
                assert msg == OOPS_TABLE[total]
