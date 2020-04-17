import json
from cached_property import cached_property
CARD_SUITS = ['C', 'D', 'S', 'H']
CARD_RANKS = ['J', '9', 'A', 'T', 'K', 'Q']

CARD_RANK_TO_VALUE_MAP = {
'J' : 3,
'9' : 2,
'A' : 1,
'T' : 1,
'K' : 0,
'Q' : 0
}

# Potentially use this to make comparison easier without messing w values
epsilon = 0.000001
CARD_RANK_TO_CMP_VALUE_MAP = {
'J' : 3,
'9' : 2,
'A' : 1 + epsilon,
'T' : 1,
'K' : 0 + epsilon,
'Q' : 0
}

class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    # Experimental
    @property
    def json(self):
        return json.dumps(self.__dict__)

def main():
    c1 = Card("J", "S")
    print (c1.json)

if __name__ == '__main__':
    main()
