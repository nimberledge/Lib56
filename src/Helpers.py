from Card import *
import random, copy

# Sorts by rank, then suit
# Also does black-red-black-red so that you don't get too confused
def sort_hand(hand):
    hand.sort(key=lambda x : CARD_RANKS.index(x.rank))
    hand.sort(key=lambda x : CARD_SUITS.index(x.suit))


if __name__ == '__main__':
    deck = []
    for suit in CARD_SUITS:
        for rank in CARD_RANKS[:-2]:
            card = Card(rank, suit)
            deck.append(card)
            deck.append(copy.deepcopy(card))
    random.shuffle(deck)
    hand = deck[:8]
    print (', '.join([str(c) for c in hand]))
    sort_hand(hand)
    print (', '.join([str(c) for c in hand]))
