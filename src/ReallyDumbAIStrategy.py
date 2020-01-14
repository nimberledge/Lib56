from PlayerStrategy import PlayerStrategy

'''Really dumb AI that follows the rules.'''
class ReallyDumbAIStrategy(PlayerStrategy):

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.team = None
        self.hand = None
        self.winning_bid = None
        self.won_bid = False
        self.revealed_trump = None
        self.hidden_trump = None

    def __str__(self):
        return self.name

    # Game engine will assign a team
    def update_team(self, team):
        self.team = team

    # Look at your cards
    def receive_initial_hand(self, hand):
        self.hand = list(hand)

    # Update yourself with the current winning bid on the board
    def update_bid_info(self, bid):
        self.winning_bid = bid
        if bid.player == self:
            self.won_bid = True

    # Always pass on bid, if enforced, bid 28
    def make_bid(self, enforce_bid=False):
        if enforce_bid:
            return 28
        return 0

    # If you've won the bidding, select a card from your hand to hide as the trump
    def select_trump(self):
        assert self.won_bid
        self.hidden_trump = self.hand[0]
        return self.hidden_trump

    # Update yourself with the next card played
    def update_round_info(self, round):
        pass

    # Choose a card from your hand to play
    # Ask for the trump if you want to
    # Game Engine will repeatedly ask you to play a card if you play invalid
    def play_card(self, starting_player=True, round_suit=None, trump_suit=None):
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
                    return Card(None, None)
                else:
                    valid_cards = list(self.hand)
        # Play randomly from the list of valid cards
        temp_card = valid_cards[random.randint(0, len(valid_cards)-1)]
        self.hand.pop(self.hand.index(temp_card))
        return temp_card

    # Update yourself on the end of the round
    def update_end_of_round_info(self, round):
        pass

    # Update yourself based on who won the last round
    def update_end_of_game_info(self, round):
        pass

    # Some way to represent the current state of the object
    @property
    def json(self):
        pass
