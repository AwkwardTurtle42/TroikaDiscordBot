'''Represents Troika's initiative tracking system'''
import random

END_OF_ROUND_TOKEN = "End The Round"


class InitiativeTracker:
    '''Represents an Initiative tracker'''
    def __init__(self):
        self.bag = []
        self.round_bag = []

    def empty(self):
        '''Empty the initiative bag'''
        self.bag.clear()

    def add_token(self, token, count=1):
        '''Add a count of tokens to the master bag'''
        for _ in range(count):
            self.bag.append(token)

    def count_token(self, token):
        '''Returns the count of tokens in the bag'''
        return self.bag.count(token)

    def count_tokens(self):
        '''Return a count of all the tokens'''
        return len(self.bag)

    def remove_token(self, token, count=1):
        '''Remove a count of tokens from the master bag. Returns actual count of tokens removed'''
        in_bag = self.count_token(token)
        to_remove = min(count, in_bag)
        for _ in range(to_remove):
            self.bag.remove(token)
        return to_remove

    def start_round(self):
        self.round_bag = self.bag.copy()
        self.round_bag.append(END_OF_ROUND_TOKEN)
        random.shuffle(self.round_bag)

    def draw_token(self):
        return self.round_bag.pop()

    def delay_token(self, token):
        '''A user can delay action, returning their token to the bag for the round'''
        self.round_bag.append(token)
        random.shuffle(self.round_bag)

    def count_round_tokens(self):
        return len(self.round_bag)
