from PlayerStrategy import PlayerStrategy
from Card import *
from Helpers import *

import logging
import random

log_format_str = "%(message)s"
logging.basicConfig(format=log_format_str, level=logging.INFO)

'''Really dumb AI that follows the rules.'''
class ReallyDumbAIStrategy(PlayerStrategy):

    def __init__(self, name):
        self.name = name
        self.number = None
        self.team = None
        self.hand = None
        self.winning_bid = None
        self.won_bid = False
        self.revealed_trump = None
        self.hidden_trump = None
        self.just_asked_for_trump = False

    def __str__(self):
        return self.name

    # Game engine will assign a team
    def update_number_and_team(self, number, team):
        self.number = number
        self.team = team
        logging.info("{} got number {} and team {}".format(self.name, self.number, self.team))

    # Look at your cards
    def receive_initial_hand(self, hand):
        self.hand = list(hand)
        sort_hand(hand)
        logging.info("{} Received hand : {}".format(self.name ,", ".join([str(card) for card in hand])))

    # Update yourself with the current winning bid on the board
    def update_bid_info(self, bid):
        if self.winning_bid is None:
            self.winning_bid = bid
            if bid.player == self:
                self.won_bid = True
            else:
                self.won_bid = False

        if bid.bid_amount > self.winning_bid.bid_amount:
            self.winning_bid = bid

            if bid.player == self:
                self.won_bid = True
            else:
                self.won_bid = False

    def display_hand(self):
        sort_hand(self.hand)
        print ('Current hand: {}'.format(','.join([str(c) for c in self.hand])))

    # Always pass on bid, if enforced, bid 28
    def make_bid(self, enforce_bid=False):
        if enforce_bid:
            return 28
        if self.winning_bid.bid_amount < 31:
            return self.winning_bid.bid_amount + 1
        return 0

    # If you've won the bidding, select a card from your hand to hide as the trump
    def select_trump(self):
        assert self.won_bid
        self.hidden_trump = self.hand[0]
        self.hand.pop(0)
        return self.hidden_trump

    def update_trump_card_info(self, trump_card):
        if self.won_bid:
            self.hand.append(self.hidden_trump)

    # Update yourself with the next card played
    def update_round_info(self, round):
        pass

    def play_card(self, round):
        if not round.round_started:
            return self.play_card_helper(trump_suit=round.trump_suit)
        else:
            return self.play_card_helper(starting_player=False, round_suit=round.round_suit, trump_suit=round.trump_suit)

    # Choose a card from your hand to play
    # Ask for the trump if you want to
    # Game Engine will repeatedly ask you to play a card if you play invalid
    def play_card_helper(self, starting_player=True, round_suit=None, trump_suit=None):
        valid_cards = []
        if starting_player:
            # Trump not been revealed
            if self.revealed_trump is None and self.won_bid:
                valid_cards = [card for card in self.hand if card.suit != self.hidden_trump.suit]
            # Trump has been revealed
            else:
                valid_cards = list(self.hand)
        else:
            # If you have cards in round_suit pick from those
            valid_cards = [card for card in self.hand if card.suit == round_suit]
            if len(valid_cards) == 0:
                # janky solution - return this sentinel card, have the GameEngine deal with it
                # Game engine will ask again anyway
                if trump_suit is None:
                    self.just_asked_for_trump = True
                    return Card(None, None)
                else:
                    # If we just asked for trump we gotta play one
                    if self.just_asked_for_trump:
                        self.just_asked_for_trump = False
                        valid_cards = [card for card in self.hand if card.suit == trump_suit]
                        if len(valid_cards) == 0:
                            valid_cards = list(self.hand)
                    else:
                        valid_cards = list(self.hand)
        # Play randomly from the list of valid cards
        if len(valid_cards) == 0:
            valid_cards = list(self.hand)
        temp_card = valid_cards[random.randint(0, len(valid_cards)-1)]
        self.hand.remove(temp_card)
        return temp_card

    # Update yourself on the end of the round
    def update_end_of_round_info(self, round):
        pass

    # Update yourself based on who won the last round
    def update_end_of_game_info(self, round):
        pass

    def reset(self):
        self.hand = None
        self.winning_bid = None
        self.won_bid = False
        self.revealed_trump = None
        self.hidden_trump = None
        self.just_asked_for_trump = False

    # Some way to represent the current state of the object
    # @property
    # def json(self):
    #     pass
