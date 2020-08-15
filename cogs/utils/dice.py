'''A place for useful utility functions'''
import random

class RollResult:
    '''A somewhat compatible class equivalent to d20'''
    def __init__(self, total, result):
        self.total = total
        self.result = result


def roll_d6():
    '''Rolls a single d6'''
    roll = random.randint(1, 6)
    return RollResult(roll, "1d6 (**roll**)")


def roll_2d6(criticals=False):
    '''Rolls 2d6. Returns first die, second die, total of both die'''
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)

    return RollResult(die1+die2, f'2d6({die1}, {die2}) = `{die1 + die2}`')


def roll_d66():
    '''Rolls a d66. Returns a single value'''
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1*10 + die2
    return RollResult(total, f'd66({die1}, {die2}) = `{total}`')
