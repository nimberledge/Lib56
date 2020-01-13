from abc import *

# Abstract base class for players. We can implement this class to get different strategy elements
class PlayerStrategy(ABC):

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return self.name

    # Game engine will assign a team
    @abstractmethod
    def update_team(self, team):
        pass

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
    # Ask for the trump if you want to
    # Game Engine will repeatedly ask you to play a card if you play invalid
    @abstractmethod
    def play_card(self):
        pass

    # Update yourself on the end of the round
    @abstractmethod
    def update_end_of_round_info(self, round):
        pass

    # Update yourself based on who won the last round
    @abstractmethod
    def update_end_of_game_info(self, round):
        pass
