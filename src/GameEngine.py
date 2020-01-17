from Card import *
from PlayerStrategy import PlayerStrategy
from Bid import Bid
from Round import Round
from Helpers import *
import copy
import random
import logging
from ReallyDumbAIStrategy import ReallyDumbAIStrategy

log_format_str = "INFO: %(message)s"
logging.basicConfig(format=log_format_str, level=logging.INFO)

class GameEngine(object):

    def __init__(self, num_players, strategies=None, randomize_start=False):
        assert num_players in [4, 6]
        logging.info("Starting game engine to play game with {} players".format(num_players))
        self.num_players = num_players
        self.player_hands = [[] for i in range(num_players)]

        # Assuming 1 is left of 0 is left of n-1, this is easy enough to do
        # Round play can now go on in this order, and it will be a rendering thing later
        if randomize_start:
            self.starting_player = random.randint(0, num_players-1)
        else:
            self.starting_player = 0
        # self.starting_player = 0
        self.trump_revealed = False
        logging.info("Set starting player : {}".format(self.starting_player))

        self.game_rounds = []

        self.teams = ["BLUE", "RED"]
        self.game_bid = None
        self.blue_overall_pts = 0
        self.red_overall_pts = 0
        # strategies as a proxy for the N PlayerStrategy-like objects representing
        # each of the players
        if strategies is not None:
            assert len(strategies) == self.num_players
            self.players = list(strategies)
            # Alternate players on the same team
            for i, player in enumerate(self.players):
                player.update_number_and_team(i, self.teams[i % 2])
            logging.info("Assigned teams and informed players of which team they are on")
        else:
            pass
            # self.players = [None for i in range(self.num_players)]

    # Generate a shuffled deck
    def generate_deck(self):
        deck = []
        if self.num_players == 4:
            logging.info("Generating 4 player deck")
            for suit in CARD_SUITS:
                # Skip Kings and Queens
                for rank in CARD_RANKS[:-2]:
                    card = Card(rank, suit)
                    deck.append(card)
                    deck.append(copy.deepcopy(card))
        else:
            logging.info("Generating 6 player deck")
            for suit in CARD_SUITS:
                for rank in CARD_RANKS:
                    card = Card(rank, suit)
                    deck.append(card)
                    deck.append(copy.deepcopy(card))
        logging.info("Shuffling deck")
        random.shuffle(deck)
        self.deck = list(deck)

    # Make the hands up, let the players know
    def deal_to_players(self):
        logging.info("Dealing cards to players")
        # For now, deal one at a time to each
        # Since our shuffle is pseudo-random library shuffle, might as well
        for i, card in enumerate(self.deck):
            self.player_hands[i % self.num_players].append(card)
        # self.deck = []
        # Let each Player look at their hand
        logging.info("Informing players of their hands")
        for i, player in enumerate(self.players):
            self.players[i].receive_initial_hand(self.player_hands[i])

    # Informs all players of the new winning bid on the table
    def push_bid_info(self, bid):
        logging.info("Sending bid info : {} bid {} to all players".format(bid.player.name, bid.bid_amount))
        for player in self.players:
            player.update_bid_info(bid)

    # Enforce rules like 28 starting bid, teammates, and termination of the round
    # At the end of the round, ask the winning bidder for a trump card to put down
    def process_bidding_round(self):
        logging.info("Starting bidding round")
        first_bidder = self.starting_player
        next_bidder = first_bidder

        # Assume bids are legal because the UI should handle this bit
        # If we do do AI players we might as well enforce they follow rules too right?
        logging.info("Getting a first bid from {}, and enforcing a minimum 28 bid".format(self.players[self.starting_player].name))
        bid_amount = self.players[first_bidder].make_bid(enforce_bid=True)
        winning_bid = Bid(self.players[first_bidder], bid_amount)
        self.push_bid_info(winning_bid)

        logging.info("Continuing bidding round after first bid")
        done = False
        last_nminus1_bids = []
        while not done:
            next_bidder = (next_bidder + 1) % self.num_players
            bid_amount = self.players[next_bidder].make_bid()
            # TODO: Implement bidding rules
            # Second condition _should_ be redundant because we should assume they play by the rules
            if bid_amount > 0 and bid_amount > winning_bid.bid_amount:
                logging.info("Updating winning bid : {} bid {}".format(self.players[next_bidder].name, bid_amount))
                winning_bid = Bid(self.players[next_bidder], bid_amount)
                self.push_bid_info(winning_bid)
            else:
                logging.info("{} opted to pass".format(self.players[next_bidder].name))
            # Check termination
            if len(last_nminus1_bids) < self.num_players-1:
                last_nminus1_bids.append(bid_amount)
            else:
                # Should use an array but lol
                last_nminus1_bids.pop(0)
                last_nminus1_bids.append(bid_amount)
            # If 3 people pass in a row
            if len(last_nminus1_bids) == self.num_players-1 and sum(last_nminus1_bids) == 0:
                logging.info("Last {} bids were passes, ending bidding round".format(self.num_players-1))
                done = True

        self.game_bid = winning_bid
        logging.info("Asking winning bidder to select a trump to hide")
        self.hidden_trump_card = winning_bid.player.select_trump()
        self.bidder_index = winning_bid.player.number
        # Remove the card from their hand, and place it face down on the table
        # Note that this card is not available to play until trump is requested
        self.player_hands[self.bidder_index].remove(self.hidden_trump_card)
        logging.info("{} chose to hide {}".format(winning_bid.player.name, str(self.hidden_trump_card)))
        # Use this to make sure the player doesn't start a round with that suit
        # (unless they have no choice but code that too)
        self.trump_suit = self.hidden_trump_card.suit

    # Game Engine should know each player's cards so we can invalidate illegal play
    # Process round should start a new round with a card from the first player,
    # poll for each of the cards, including if players ask for and reveal the trump,
    # and compute a round-winner so that we can determine the start of the next round
    # Also maybe pass on the round information to all players in software / probably give
    # updates to that info with each card played

    # Run all 8 rounds of this, calling play_round for each.
    def play_all_rounds(self):
        round_starter_index = self.starting_player
        num_rounds = 0
        rounds = []
        while num_rounds < 8:
            num_rounds += 1
            logging.info("Beginning round {}".format(num_rounds))
            if self.trump_revealed:
                round = Round(trump_suit=self.trump_suit)
            else:
                round = Round()
            self.play_round(round, round_starter_index)
            round_starter_index = round.winning_player.number
            rounds.append(round)
            # Let all players know what happened here
            for player in self.players:
                player.update_end_of_round_info(round)
            logging.info("Round {} won by {}".format(num_rounds, round.winning_player.name))
        self.game_rounds = list(rounds)

    def play_round(self, round, start_index):
        turns = 0
        next_player = self.players[start_index]
        while turns < self.num_players:
            self.play_turn(round, next_player)
            turns += 1
            next_player = self.players[(start_index + turns) % self.num_players]

    # Make sure player asking for trump is not breaking rules
    # Actually this could be done via the UI
    def valid_trump_request(self, player, round):
        logging.info("Validating trump request from {}".format(player.name))
        if self.trump_revealed:
            logging.info("Invalid trump request from {}, trump already revealed".format(player.name))
            return False
        index = player.number
        player_hand = self.player_hands[index]
        suit_cards = [card for card in player_hand if card.suit == round.round_suit]
        if len(suit_cards) == 0:
            logging.info("Valid trump request from {}".format(player.name))
            return True
        else:
            logging.info("Invalid trump request from {}".format(player.name))
            return False

    # Recurses until the player has played a valid card
    # Maybe unnecessary (?) assume they play by the rules and then
    # we have player_card = player.play_card(round)
    # round.update_round(player_card)
    def play_turn(self, round, player, enforce_suit=None):
        # logging.info("Querying {} for card".format(player.name))
        player_card = player.play_card(round)
        # logging.info("{} tried to play {}".format(player.name, str(player_card)))
        # assert player_card in self.player_hands[player.number]
        if round.round_started:
            # If player requests trump
            if player_card == Card(None, None):
                logging.info("{} requests trump".format(player.name))
                if self.valid_trump_request(player, round):
                    # Reveal the trump and broadcast it to all players
                    self.reveal_trump()
                    round.reveal_trump(self.trump_suit)
                    # Enforce that the player plays a trump card
                    self.play_turn(round, player, enforce_suit=self.trump_suit)
                else: # idk do the request in a loop??
                    # Since we're not updating the round info seems legit to recurse
                    logging.info("Bad trump request from {}".format(player.name))
                    self.play_turn(round, player)
                    pass
            # Round has started, player didn't request trump
            else:
                if enforce_suit is not None:
                    # If player cheats and doesn't a play a trump even tho they have one
                    if player_card.suit != enforce_suit:
                        if len([card for card in self.player_hands[player.number] if card.suit==enforce_suit]) > 0:
                            self.play_turn(round, player, enforce_suit)
                round.update_round(player, player_card)
                self.player_hands[player.number].remove(player_card)
        # If round hasn't yet begun
        else:
            # No requesting trump if it's the start of the round...
            if player_card == Card(None, None):
                self.play_turn(round, player)
            # Round has not yet begun, ensure the player does not start w trump unless revealed or
            # they have no other option
            if player.number == self.bidder_index and not self.trump_revealed:
                if player_card.suit == self.trump_suit:
                    if len([card for card in self.player_hands[player.number] if card.suit != self.trump_suit]) > 0:
                        self.play_turn(round, player)
            round.update_round(player, player_card)
            self.player_hands[player.number].remove(player_card)

    # Update whatever needs to be updated and inform all players of what the trump is
    def reveal_trump(self):
        self.trump_revealed = True
        self.player_hands[self.bidder_index].append(self.hidden_trump_card)
        # self.hidden_trump_card = None
        for player in self.players:
            player.update_trump_card_info(self.hidden_trump_card)
        self.hidden_trump_card = None

    # Determine if the bidder made their bid, and how many points go to which team
    def determine_game_points(self):
        logging.info("Game has ended, points being tallied")
        blue_pts, red_pts = 0, 0
        # Total the points
        for round in self.game_rounds:
            if round.winning_player.team == "BLUE":
                blue_pts += round.round_pts
            else:
                red_pts += round.round_pts

        # Points modifier for bids 40 and above
        bid_pad = 0
        if self.game_bid.bid_amount >= 40:
            bid_pad += 1
        if self.players[self.bidder_index].team == "BLUE":
            if blue_pts >= self.game_bid.bid_amount:
                self.blue_overall_pts += 1 + bid_pad
                logging.info("Blue team won their bid, getting {} points".format(1 + bid_pad))
            else:
                self.red_overall_pts += 2 + bid_pad
                logging.info("Blue team failed to make their bid, earning Red team {} points".format(2 + bid_pad))
        else:
            if red_pts >= self.game_bid.bid_amount:
                self.red_overall_pts += 1 + bid_pad
                logging.info("Red team won their bid, getting {} points".format(1 + bid_pad))
            else:
                self.blue_overall_pts += 2 + bid_pad
                logging.info("Red team failed to make their bid, earning Blue team {} points".format(2 + bid_pad))
        logging.info("Overall score: Red {} - Blue {}".format(self.red_overall_pts, self.blue_overall_pts))
    # Reset all game-specific params so that we can have the next game
    # shift the starting player one to the left
    # reset all players
    def reset_game(self):
        logging.info("Resetting GameEngine state")
        self.player_hands = [[] for i in range(self.num_players)]
        self.starting_player = (self.starting_player + 1) % self.num_players
        self.trump_revealed = False
        self.game_rounds = []
        self.game_bid = None
        logging.info("Asking players to reset state")
        for player in self.players:
            player.reset()

    # Whole game, bidding to round-play, to determining overall points
    def play_game(self):
        self.generate_deck()
        self.deal_to_players()
        self.process_bidding_round()
        self.play_all_rounds()
        self.determine_game_points()
        self.reset_game()

def test_main():
    # ge_6 = GameEngine(num_players=6)
    player_1 = ReallyDumbAIStrategy("Player 1")
    player_2 = ReallyDumbAIStrategy("Player 2")
    player_3 = ReallyDumbAIStrategy("Player 3")
    player_4 = ReallyDumbAIStrategy("Player 4")
    # player_5 = ReallyDumbAIStrategy("Player 5")
    # player_6 = ReallyDumbAIStrategy("Player 6")
    # strategies = [player_1, player_2, player_3, player_4, player_5, player_6]
    strategies = [player_1, player_2, player_3, player_4]
    # ge_6 = GameEngine(num_players=6, strategies=strategies, randomize_start=True)
    # ge_6.play_game()
    ge_4 = GameEngine(num_players=4, strategies=strategies, randomize_start=True)
    ge_4.play_game()
    ge_4.play_game()
    # ge_4.generate_deck()
    # for card in ge_4.deck:
    #     print (card)
    # print (len(ge_4.deck), end='\n\n')
    # ge_6.generate_deck()
    # for card in ge_6.deck:
    #     print (card)
    # print (len(ge_6.deck), end='\n\n')

if __name__ == '__main__':
    test_main()
