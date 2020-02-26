from PlayerStrategy import PlayerStrategy
from Card import *
from Helpers import *

import logging
import random

log_format_str = "%(message)s"
logging.basicConfig(format=log_format_str, level=logging.INFO)

'''Colloquial wisdom boiled down to the basics.'''
class HeuristicStrategy(PlayerStrategy):
    WEAK_TRUMP_STRENGTH = 1
    STRONG_TRUMP_STRENGTH = 2
    VERY_STRONG_TRUMP_STRENGTH = 3
    TRUMP_JACK_STRENGTH = 1
    PARTNER_STARTING_STRENGTH = 1 # Add randomness to this, so its sometimes 2 sometimes 0
    SHAKE_JACK_STRENGTH = 0
    OTHER_JACK_STRENGTH = 1
    # Multiply by this for every cut color, add to hand_strength
    CUT_COLOR_MULTIPLIER = 1
    # Based on suit distribution, mainly to select trump
    # 2,2,2,2 is -1 because no cut realistically
    # 33XX is -0.5 because you probably have a good support hand, disincentivize a bid a little
    # Maybe 0.5 if 3, 3, 2 and -0.5 if 3, 3, 1, 1
    # 44 is pro but in this consideration 1, because I add 2 *k for 2 cuts and +1 for 4 trumps
    DIST_2222_STRENGTH = -1
    DIST_332_STRENGTH = 0
    DIST_3311_STRENGTH = -1
    DIST_44_STRENGTH = 1

    FOUR_TRUMP_BONUS_PT = 8
    FIVE_TRUMP_BONUS_PT = 9
    SIX_TRUMP_BONUS_PT = 10

    TWO_TRUMP_STRENGTH = 1
    THREE_TRUMP_STRENGTH = 2
    FOUR_TRUMP_STRENGTH = 2.5
    FIVE_TRUMP_STRENGTH = 3.5
    SIX_TRUMP_STRENGTH = 4.5

    TRUMP_WITHOUT_JACK_STRENGTH = -1
    NINE_WITH_JACK_STRENGTH = 0.5
    # NINE_WITHOUT_JACK_STRENGTH = -1

    ALPHA = 0.25
    BETA = 1

    BETTING_40_STRENGTH_CUTOFF = 8.5
    BETTING_TANI_STRENGTH_CUTOFF = 14

    def __init__(self, name):
        self.name = name
        self.number = None
        self.team = None
        self.hand = None
        self.hand_strength = 0
        self.winning_bid = None
        self.won_bid = False
        self.revealed_trump = None
        self.hidden_trump = None
        self.just_asked_for_trump = False
        self.starting_player = 0
        self.max_bid = 0

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
        self.winning_bid = bid
        if bid.player == self:
            self.won_bid = True

    def display_hand(self):
        sort_hand(self.hand)
        print ('Current hand: {}'.format(','.join([str(c) for c in self.hand])))

    def compute_max_bid(self):
        if self.max_bid != 0:
            return self.max_bid
        distribution = dict(zip(CARD_SUITS, [0 for c in CARD_SUITS]))
        for card in self.hand:
            distribution[card.suit] += 1
        print ("Suit distribution: {}".format(distribution))
        best_suits = list(CARD_SUITS)
        best_suits.sort(key=lambda x: distribution[x], reverse=True)
        print ("Best suits {}\n{}".format(best_suits, [distribution[s] for s in best_suits]))
        best_suit = best_suits[0]
        if distribution[best_suits[0]] == distribution[best_suits[1]]:
            # We have a tie
            # Could be 2,2,2,2 3,3,X,X 4,4
            # distinguished by how many there are beautiful
            if distribution[best_suits[0]] == 2:
                self.hand_strength += self.DIST_2222_STRENGTH
            elif distribution[best_suits[0]] == 3 and distribution[best_suits[2]] == 2:
                self.hand_strength += self.DIST_332_STRENGTH
            elif distribution[best_suits[0]] == 3 and distribution[best_suits[2]] == 1:
                self.hand_strength += self.DIST_3311_STRENGTH
            else: # 4 but its vacuous because enumeration
                self.hand_strength += self.DIST_44_STRENGTH

        num_cut_colors = 4 - len(set([c.suit for c in self.hand]))
        self.hand_strength += num_cut_colors * self.CUT_COLOR_MULTIPLIER
        print ("number of cut colors: {}".format(num_cut_colors))

        # Now we figure out which one to make our trump
        # I think using a list handles all situations
        # suits_considered = [suit for suit in best_suits if distribution[suit] == distribution[best_suit]]
        trump_ratings = [0 for suit in CARD_SUITS]
        for i, suit in enumerate(CARD_SUITS):
            trump_pts = sum([CARD_RANK_TO_VALUE_MAP[c.rank] for c in self.hand if c.suit == suit])
            # trump_ratings[i] += trump_pts
            if distribution[suit] == 2:
                trump_ratings[i] += self.TWO_TRUMP_STRENGTH
            if distribution[suit] == 3:
                trump_ratings[i] += self.THREE_TRUMP_STRENGTH
            if distribution[suit] == 4: # If you have 4 trump
                trump_ratings[i] += self.FOUR_TRUMP_STRENGTH
                # if trump_pts > self.FOUR_TRUMP_BONUS_PT:
                #     print ("Strong trump bonus")
                #     trump_ratings[i] += 1
            if distribution[suit] == 5: # If you have 5 trump
                trump_ratings[i] += self.FIVE_TRUMP_STRENGTH
                if trump_pts > self.FIVE_TRUMP_BONUS_PT:
                    trump_ratings[i] += 1
            if distribution[suit] == 6: # If you have 6 trump
                trump_ratings[i] += self.SIX_TRUMP_STRENGTH
                if trump_pts > self.SIX_TRUMP_BONUS_PT:
                    trump_ratings[i] += 1
            else:
                # Insanely OP hand probz wanna go tani lmao
                trump_ratings[i] += distribution[suit]
        best_suit = CARD_SUITS[trump_ratings.index(max(trump_ratings))]
        self.hand_strength += max(trump_ratings)
        print ("Hand strength, best_suit: ", self.hand_strength, best_suit)
        # We've figured out our trump strength let's figure out raw strength
        trump_cards = [card for card in self.hand if card.suit == best_suit]
        if max([CARD_RANK_TO_VALUE_MAP[c.rank] for c in trump_cards]) != 3: # Trump without jack
            self.hand_strength += self.TRUMP_WITHOUT_JACK_STRENGTH
        self.heuristic_strength = self.hand_strength
        self.winners = 0
        # +1 for every winner
        for card in self.hand:
            if card.suit == best_suit:
                self.winners += 1
            elif card.rank == 'J':
                if distribution[card.suit] == 1: # Shake jack
                    self.winners += self.SHAKE_JACK_STRENGTH
                    # print ("Shake jack")
                else:
                    self.winners += self.OTHER_JACK_STRENGTH
                    # print ("Other jack")
            elif card.rank == '9':
                if distribution[card.suit] <= 2:
                    continue
                if max([CARD_RANK_TO_VALUE_MAP[c.rank] for c in self.hand if c.suit == card.suit]) == 3:
                    self.winners += self.NINE_WITH_JACK_STRENGTH

        print ("Winners: {}".format(self.winners))
        self.hand_strength = self.ALPHA * self.heuristic_strength + self.BETA * self.winners
        print ("Final hand_strength: {}".format(self.hand_strength))
        # So I wanna determine a max_bid, and compute it only once.
        # If my max bid is tani should just bid tani
        # If my max bid is in 40-55 range should bid max(40, current_bid+1)
        # If my bid is in 28-39 range, obv don't outbid a teammate, and bid greedy
        self.max_bid = int(self.hand_strength * 5.5)
        if self.max_bid < 28:
            self.max_bid = 28
        if self.max_bid > 56:
            self.max_bid = 56

        self.bid_region = 0
        if 28 <= self.max_bid <= 39:
            self.bid_region = 0
        elif 40 <= self.max_bid <= 55:
            self.bid_region = 1
        else:
            self.bid_region = 2

        print ("Max bid: ", self.max_bid)

    def make_bid(self, enforce_bid=False):
        self.compute_max_bid()
        print ("Current winning bid:{}".format(self.winning_bid))
        if enforce_bid:
            if self.bid_region == 0:
                return 28
            elif self.bid_region == 1:
                return 40
            else:
                return 56
        # Then bid
        if self.winning_bid.bid_amount < self.max_bid:
            if self.winning_bid.player.number % 2 == self.number % 2:
                if self.winning_bid.bid_amount < 40:
                    if self.bid_region == 0:
                        return 0
                    elif self.bid_region == 1:
                        return 40
                    else:
                        return 56
                else:
                    return self.winning_bid.bid_amount + 1
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
    @property
    def json(self):
        pass


def test_main():
    player1 = HeuristicStrategy("Deeeb")
    hand_str = ['JS', 'JS', 'AS', 'TS', '9S', 'TC', 'JH', 'JD']
    hand = [Card(c[0], c[1]) for c in hand_str]
    player1.update_number_and_team(1, 'RED')
    player1.receive_initial_hand(hand)
    print(player1.make_bid(enforce_bid=True))


if __name__ == '__main__':
    test_main()
