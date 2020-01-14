from Card import *
from PlayerStrategy import PlayerStrategy
from Helpers import *
import copy
import random

class GameEngine(object):

    def __init__(self, num_players, strategies=None, randomize_start=False):
        assert num_players in [4, 6]

        self.num_players = num_players
        self.player_hands = [[] for i in range(num_players)]

        # Assuming 1 is left of 0 is left of n-1, this is easy enough to do
        # Round play can now go on in this order, and it will be a rendering thing later
        # if randomize_start:
        #     self.starting_player = random.randint(0, num_players-1)
        # else:
        #     self.starting_player = 0
        self.starting_player = 0

        self.teams = ["BLUE", "RED"]
        # strategies as a proxy for the N PlayerStrategy-like objects representing
        # each of the players
        if strategies is not None:
            assert len(strategies) == self.num_players
            self.players = list(strategies)
            # Alternate players on the same team
            for i, player in enumerate(self.players):
                player.update_team(self.teams[i % 2])
        else:
            pass
            # self.players = [None for i in range(self.num_players)]

    # Generate a shuffled deck
    def generate_deck(self):
        deck = []
        if self.num_players == 4:
            for suit in CARD_SUITS:
                # Skip Kings and Queens
                for rank in CARD_RANKS[:-2]:
                    card = Card(rank, suit)
                    deck.append(card)
                    deck.append(copy.deepcopy(card))
        else:
            for suit in CARD_SUITS:
                for rank in CARD_RANKS:
                    card = Card(rank, suit)
                    deck.append(card)
                    deck.append(copy.deepcopy(card))
        random.shuffle(deck)
        self.deck = list(deck)

    # Make the hands up, let the players know
    def deal_to_players(self):
        # For now, deal one at a time to each
        # Since our shuffle is pseudo-random library shuffle, might as well
        for i, card in enumerate(self.deck):
            self.player_hands[i % num_players].append(card)
        # Let each Player look at their hand
        for i, player in enumerate(self.players):
            self.players[i].receive_initial_hand(self.player_hands[i])

    # Informs all players of the new winning bid on the table
    def push_bid_info(self, bid):
        for player in self.players:
            player.update_bid_info(bid)

    # Enforce rules like 28 starting bid, teammates, and termination of the round
    # At the end of the round, ask the winning bidder for a trump card to put down
    def process_bidding_round(self):
        first_bidder = self.starting_player
        next_bidder = first_bidder
        bid_amount = self.players[first_bidder].make_bid(enforce_bid=True)
        winning_bid = Bid(self.players[first_bidder], bid_amount)
        self.push_bid_info(winning_bid)
        done = False
        last_three_bids = []
        while not done:
            next_bidder = (next_bidder + 1) % num_players
            bid_amount = self.players[next_bidder].make_bid()
            # TODO: Implement bidding rules
            if bid_amount > 0 and bid_amount > winning_bid.bid_amount:
                winning_bid = Bid(self.players[next_bidder], bid_amount)
                self.push_bid_info(winning_bid)

            # Check termination
            if len(last_three_bids) < 3:
                last_three_bids.append(bid_amount)
            else:
                last_three_bids.pop(0)
                last_three_bids.append(bid_amount)
            # If 3 people pass in a row
            if sum(last_three_bids) == 0:
                done = True
        self.game_bid = winning_bid
        self.hidden_trump_card = winning_bid.player.select_trump()
        self.bidder_index = winning_bid.player.number
        # Use this to make sure the player doesn't start a round with that suit
        # (unless they have no choice but code that too)
        self.trump_suit = self.hidden_trump_card.suit
        # Make sure they don't give you a bogus card, lol
        assert (self.hidden_trump_card in self.player_hands[winning_bid.player.number])

    # Game Engine should know each player's cards so we can invalidate illegal play
    # Process round should start a new round with a card from the first player,
    # poll for each of the cards, including if players ask for and reveal the trump,
    # and compute a round-winner so that we can determine the start of the next round
    # Also maybe pass on the round information to all players in software / probably give
    # updates to that info with each card played
    def process_round(self):
        pass

    # Make sure player asking for trump is not breaking rules
    def process_trump_request(self):
        pass

    # Update whatever needs to be updated and inform all players of what the trump is
    def reveal_trump(self):
        pass

    # Run all 8 rounds of this, calling process_round for each.
    def process_all_rounds(self):
        first_starter = self.starting_player
        next_starter = first_starter
        pass

    # Determine if the bidder made their bid, and how many points go to which team
    def determine_game_points(self):
        pass

    # Reset all game-specific params so that we can have the next game
    # shift the starting player one to the left
    def reset_game(self):
        pass


def test_main():
    ge_4 = GameEngine(num_players=4)
    ge_6 = GameEngine(num_players=6)
    # ge_4.generate_deck()
    # for card in ge_4.deck:
    #     print (card)
    # print (len(ge_4.deck), end='\n\n')
    # ge_6.generate_deck()
    # for card in ge_6.deck:
    #     print (card)
    # print (len(ge_6.deck), end='\n\n')
    c1 = Card('Q', 'C')
    c2 = Card('A', 'C')
    # Use this to test extensively
    print (card_compare(c1, c2, 'D', 'C'))

if __name__ == '__main__':
    test_main()
