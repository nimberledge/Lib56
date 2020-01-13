from PlayerStrategy import PlayerStrategy
from Helpers import *

class HumanPlayerStrategy(PlayerStrategy):

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.trump_suit = None
        self.hand = []
        self.current_winning_bid = None
        self.hidden_card = None

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
        self.current_winning_bid = copy.deepcopy(bid)

    def display_hand(self):
        sort_hand(self.hand)
        print ('Current hand: {}'.format(', '.join[str(c) for c in self.hand]))
        if self.hidden_card:
            print ('(Trump) Card hidden: ', self.hidden_card)

    # Make the next bid, enforce_bid for first bid, otherwise pass is possible
    # Return an int, the bid amount. Return 0 if passing.
    def make_bid(self, enforce_bid=False):
        self.display_hand()
        print ('Current bid amount: {}'.format(self.current_winning_bid.bid_amount))
        valid_bid = False
        while not valid_bid:
            bid_amount =  int(input('Enter amount to bid: '))
            if bid_amount < 28 and enforce_bid:
                print ('Invalid bid, try again. It is the first bid and you must bid a minimum of 28')
            elif bid_amount <= self.current_winning_bid.bid_amount and bid_amount > 0:
                print ('Invalid bid, try again')
            else:
                valid_bid = True
        return bid_amount

    # If you've won the bidding, select a card from your hand to hide as the trump
    def select_trump(self):
        self.display_hand()
        valid_card = False
        temp_card = None
        while not valid_card:
            card_str = input('Enter the card to put down as trump: ')
            if len(card_str) < 2:
                print ('Invalid card')
                continue
            rank, suit = card_str[0], card_str[1]
            temp_card = Card(rank, suit)
            if temp_card in self.hand:
                valid_card = True
            else:
                print ('Invalid card')
        return temp_card


    # Update yourself with the next card played
    def update_round_info(self, round):
        pass

    # Choose a card from your hand to play
    # Ask for the trump if you want to
    # Game Engine will repeatedly ask you to play a card if you play invalid
    def play_card(self):
        self.display_hand()
        valid_card = False
        temp_card = None
        while not valid_card:
            card_str = input('Enter the card to play: ')

    # Update yourself on the end of the round
    @abstractmethod
    def update_end_of_round_info(self, round):
        pass

    # Update yourself based on who won the last round
    @abstractmethod
    def update_end_of_game_info(self, round):
        pass
