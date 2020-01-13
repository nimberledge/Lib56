from Card import *
from PlayerStrategy import PlayerStrategy

class GameEngine(object):

    def __init__(self, num_players, strategies=None):
        # self.deck = []
        # self.players = []
        # self.starting_player = None
        # self.bids = None
        # self.teams = [BLUE, RED] # idk, something
        pass

    @staticmethod
    def card_compare(first, second, round_suit, trump=None):
        # Always compare as earlier vs later
        # Return higher card
        pass

    # Generate a shuffled deck
    def generate_deck(self):
        pass

    # Make the hands up
    def deal_to_players(self):
        pass

    # Take in the next bid, update who has the bid if necessary
    def process_bid(self):
        pass

    # Enforce rules like 28 starting bid, teammates, and termination of the round
    # At the end of the round, ask the winning bidder for a trump card to put down
    def process_bidding_round(self):
        pass

    # Game Engine should know each player's cards so we can invalidate illegal play
    # Process round should start a new round with a card from the first player,
    # poll for each of the cards, including if players ask for and reveal the trump,
    # and compute a round-winner so that we can determine the start of the next round
    # Also maybe pass on the round information to all players in software / probably give
    # updates to that info with each card played
    def process_round(self):
        pass

    # Run all 8 rounds of this, calling process_round for each.
    def process_all_rounds(self):
        pass

    # Determine if the bidder made their bid, and how many points go to which team
    def determine_game_points(self):
        pass

    # Reset all game-specific params so that we can have the next game
    # shift the starting player one to the left
    def reset_game(self):
        pass
