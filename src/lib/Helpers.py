from Card import *
import random, copy

# Sorts by rank, then suit
# Also does black-red-black-red so that you don't get too confused
# Shapes are hard ok - Rithi
def sort_hand(hand):
    hand.sort(key=lambda x : CARD_RANKS.index(x.rank))
    hand.sort(key=lambda x : CARD_SUITS.index(x.suit))

def card_compare(first, second, round_suit, trump_suit=None):
    # Always compare as earlier vs later
    # Return -1 if second > first, 1 if first > second, 0 otherwise
    # If round_suit and trump_suit are the same, can compare pretending
    # trump_suit is None essentially
    # If someone throws a trump before it's revealed, it is not a cut
    # but GameEngine mechanics can be to only compare winning card with new card
    # in which case this would be ok
    # additional case to avoid duplicating code is checking that either card is a trump
    # if not, then the first compare suffices
    if (trump_suit is None) or (round_suit == trump_suit) or (trump_suit not in [first.suit, second.suit]):
        if first.suit == round_suit and second.suit != round_suit:
            return 1
        elif second.suit == round_suit and first.suit != round_suit:
            return -1
        elif first.suit != round_suit and second.suit != round_suit:
            return 0
        else:
            # >= and not > because first is earlier
            if CARD_RANK_TO_CMP_VALUE_MAP[first.rank] >= CARD_RANK_TO_CMP_VALUE_MAP[second.rank]:
                return 1
            else:
                return -1
    else:
        # If one is trump and the other is not, then
        if first.suit == trump_suit and second.suit != trump_suit:
            return 1
        elif second.suit == trump_suit and first.suit != trump_suit:
            return -1
        # Both are trumps
        else:
            if CARD_RANK_TO_CMP_VALUE_MAP[first.rank] >= CARD_RANK_TO_CMP_VALUE_MAP[second.rank]:
                return 1
            else:
                return -1

# Takes in a hand and returns all the cards that you could potentially play
# If the round_suit hasn't yet been decided, all cards are valid (first card in round)
def valid_cards(hand, round_suit=None, trump_requested=False, trump_suit=None):
    if round_suit is None:
        return hand
    if round_suit not in [card.suit for card in hand]:
        return hand
    else:
        return [card for card in hand if card.suit == round_suit]

    if trump_requested and trump_suit:
        if trump_suit not in [card.suit for card in hand]:
            return hand
        else:
            return [card for card in hand if card.suit==trump_suit]

    return hand


if __name__ == '__main__':
    # deck = []
    # for suit in CARD_SUITS:
    #     for rank in CARD_RANKS[:-2]:
    #         card = Card(rank, suit)
    #         deck.append(card)
    #         deck.append(copy.deepcopy(card))
    # random.shuffle(deck)
    # hand = deck[:8]
    # print (', '.join([str(c) for c in hand]))
    # sort_hand(hand)
    # print (', '.join([str(c) for c in hand]))
    c1 = Card('J', 'C')
    c2 = Card('J', 'C')
    # Use this to test
    # args - earlier card, later card, round suit, trump suit (use None if trump hidden)
    print (card_compare(c1, c2, 'D', 'C'))
