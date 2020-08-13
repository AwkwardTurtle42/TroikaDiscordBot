'''Represents Troika's initiative tracking system'''
import random


END_OF_ROUND_TOKEN = "<<End The Round>>"


class InitiativeTracker:
    '''Represents an Initiative tracker'''
    def __init__(self):
        self.bag = []
        self.in_round = False
        self.round_bag = []
        self.round_num = 0
        self.round_last_drawn = None
        self.drawn_log = []

    def empty(self):
        '''Empty the initiative bag'''
        self.bag.clear()
        self.round_bag = []
        self.in_round = False
        self.round_num = 0
        self.round_last_drawn = None
        self.drawn_log = []

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

    def display_tokens(self):
        counts = {}
        for token in self.bag:
            if token not in counts:
                counts[token] = 0
            counts[token] += 1

        output_string = ""
        for key in sorted(counts):
            output_string += f"{key}({counts[key]}) "

        return output_string.rstrip()

    def shuffle_tokens(self):
        if self.in_round:
            random.shuffle(self.round_bag)

    def start_round(self):
        self.round_bag = self.bag.copy()
        self.round_bag.append(END_OF_ROUND_TOKEN)
        self.shuffle_tokens()
        self.round_num += 1
        self.drawn_log.append([])
        self.in_round = True

    def draw_token(self):
        if not self.in_round:
            return END_OF_ROUND_TOKEN

        token = self.round_bag.pop(0)
        if token == END_OF_ROUND_TOKEN:
            self.in_round = False

        self.drawn_log[-1].append(token)
        return token

    def current_token(self):
        if not self.in_round:
            return END_OF_ROUND_TOKEN
        return self.drawn_log[-1][-1]

    def current_round_history(self):
        if not self.in_round:
            return END_OF_ROUND_TOKEN
        return self.drawn_log[-1]

    def delay_token(self, token):
        '''A user can delay action, returning their token to the bag for the round'''
        if self.in_round:
            self.round_bag.append(token)
            self.shuffle_tokens()

    def count_round_tokens(self):
        return len(self.round_bag)
