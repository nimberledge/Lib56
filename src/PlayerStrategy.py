from abc import *

# Abstract base class for players. We can implement this class to get different strategy elements
class PlayerStrategy(ABC):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    # Game engine will assign a team
    def update_number_and_team(self, number, team):
        self.number = number
        self.team = team

    # Look at your cards
    @abstractmethod
    def receive_initial_hand(self, hand):
        pass

    # Update yourself with the current winning bid on the board
    @abstractmethod
    def update_bid_info(self, bid):
        pass

    # Make the next bid, enforce_bid for first bid, otherwise pass is possible
    # Return an int, the bid amount. Return 0 if passing.
    @abstractmethod
    def make_bid(self, enforce_bid=False):
        pass

    # If you've won the bidding, select a card from your hand to hide as the trump
    @abstractmethod
    def select_trump(self):
        pass

    # Update yourself with the next card played
    @abstractmethod
    def update_round_info(self, round):
        pass

    # Choose a card from your hand to play
    # Ask for the trump if you want to by returning Card(None, None)
    # Game Engine will repeatedly ask you to play a card if you play invalid (?)
    # More likely we'll just block illegal moves from UI
    @abstractmethod
    def play_card(self, round):
        pass

    # The trump card was just requested, update yourself on what it was
    @abstractmethod
    def update_trump_card_info(self, trump_card):
        pass

    # Update yourself on the end of the round
    @abstractmethod
    def update_end_of_round_info(self, round):
        pass

    # Reset yourself at the end of the game to prep for a next one
    @abstractmethod
    def reset(self):
        pass

    # Some way to represent the current state of the object
    @property
    @abstractmethod
    def json(self):
        pass
