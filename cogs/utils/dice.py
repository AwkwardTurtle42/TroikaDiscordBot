'''A place for useful utility functions'''
import random


class RollResult:
    '''A somewhat compatible class equivalent to d20'''

    def __init__(self, total, result):
        self.total = total
        self.result = result


def roll_d3():
    """Rolls a single d3"""
    return random.randint(1, 3)


def roll_d6():
    '''Rolls a single d6'''
    return random.randint(1, 6)


def roll_2d6():
    '''Rolls 2d6. Returns first die, second die, total of both die'''
    die1 = roll_d6()
    die2 = roll_d6()

    return die1, die2, die1 + die2


def roll_under(target):
    d1, d2, total = roll_2d6()
    if total <= target:
        return RollResult(total, f"**SUCCESS** 2d6({d1}+{d2}) = `{total}` ≤ `{target}`")
    else:
        return RollResult(total, f"**FAILURE** 2d6({d1}+{d2}) = `{total}` > `{target}`")


def roll_d66():
    '''Rolls a d66. Returns a single value'''
    die1 = roll_d6()
    die2 = roll_d6()
    total = (die1 * 10) + die2
    return total
