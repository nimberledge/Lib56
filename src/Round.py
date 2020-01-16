from Card import *
from Helpers import *
import logging

log_format_str = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format_str, level=logging.INFO)

class Round(object):

    # trump_suit = None corresponds to hidden trump
    def __init__(self, trump_suit=None):
        self.trump_suit = trump_suit
        self.cards_played = []
        self.winning_card = None
        self.winning_player = None
        self.round_started = False
        self.round_suit = None
        self.round_pts = 0

    def update_round(self, player, next_card):
        logging.info("{} played the {}".format(player.name, str(next_card)))
        self.cards_played.append(next_card)
        self.round_pts += CARD_RANK_TO_VALUE_MAP[next_card.rank]
        if not self.round_started:
            self.winning_card = next_card
            self.winning_player = player
            self.round_started = True
            self.round_suit = next_card.suit
        else:
            if card_compare(self.winning_card, next_card, self.round_suit, self.trump_suit) == -1:
                self.winning_card = next_card
                self.winning_player = player


    def reveal_trump(self, trump_suit):
        assert self.trump_suit is None
        self.trump_suit = trump_suit
