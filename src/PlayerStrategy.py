class PlayerStrategy(object):

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.hand = []
        self.team = None
        pass

    def __str__(self):
        return self.name

    # Game engine will assign a team
    def update_team(self, team):
        self.team = team

    # Look at your cards
    def receive_initial_hand(self, hand):
        pass

    # Update yourself with the current winning bid on the board
    def update_bid_info(self, bid):
        pass

    # Make the next bid, enforce_bid for first bid, otherwise pass is possible
    # Return an int, the bid amount. Return 0 if passing.
    def make_bid(self, enforce_bid=False):
        pass

    # If you've won the bidding, select a card from your hand to hide as the trump
    def select_trump(self):
        pass

    # Update yourself with the next card played
    def update_round_info(self, round):
        pass

    # Choose a card from your hand to play
    # Ask for the trump if you want to
    # Game Engine will repeatedly ask you to play a card if you play invalid
    def play_card(self):
        pass

    # Update yourself on the end of the round
    def update_end_of_round_info(self, round):
        pass

    # Update yourself
    def update_end_of_game_info(self, round):
        pass
