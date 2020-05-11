"""
This module provides classes to encapsulate one ongoing game and its players.
"""

import random

from abc import ABCMeta, abstractmethod
from enum import Enum, auto as iota

from lib.PlayerStrategy import PlayerStrategy
from lib.GameEngine import GameEngine


class Card(object):
    class Suit(Enum):
        Club = iota()
        Diamond = iota()
        Spade = iota()
        Heart = iota()

    class Face(Enum):
        Ace = iota()
        Nine = iota()
        Ten = iota()
        Jack = iota()
        Queen = iota()
        King = iota()

   def __init__(suit, face):
        super().__init__()
        self.suit = suit
        self.face = face

    def value(self):
        return {
            Card.Face.Jack: (3, 0),
            Card.Face.Nine: (2, 0),
            Card.Face.Ace: (1, 1),
            Card.Face.Ten: (1, 0),
            Card.Face.Queen: (0, 1),
            Card.Face.King: (0, 0)
        }[self.face]


class Team(object):
    def __init__(self, game, players):
        super().__init__()
        self.game = game
        self.players = players

    def compute_score(self):
        return sum((p.score for p in self.players))


class Player(PlayerStrategy, metaclass=ABCMeta):
    def __init__(self, game, name):
        super().__init__(name)
        self.game = game
        self.hand = []
        self.score = 0

    def dealt(self, cards)
        self.hand += cards

    # `bid` returns 0 if the Player passes and a number between 28 and 56
    # otherwise indicating the player's bid. This number must exceed
    # `highest_bid_so_far`.
    def bid(self, highest_bid_so_far) -> int:
        def try_play(feedback=None):
            bid_score = self.on_bid(highest_bid_so_far, feedback=feedback)

            if bid_score < highest_bid_so_far or 56 < bid_score:
                return try_play(feedback=f"invalid bid (requires {highest_bid_so_far} <= bid <= 56): {bid_score}")

            return bid_score

        return bid_score

    def select_trump(self) -> Card:
        trump_card_index = self.on_select_trump()
        return self.remove_card_from_hand(trump_card_index)

    def play(self, round_index, turn_index) -> Card:
        def has_card_in_suit(suit):
            return suit in {card.suit for card in self.hand}

        def try_play(feedback=None)
            play_card_index = self.on_play(round_index, turn_index, feedback=feedback)
            trump_suit_requested = play_card_index < 0

            # If the trump suit was requested (instead of playing a card), we check
            # validity and return 'None' rather than a card if successful.
            if trump_suit_requested:
                # We don't allow requesting the trump card on the first turn (if you are the first
                # player in a round).
                if round_index == 0 and turn_index == 0:
                    return try_play(feedback=f"cannot request a trump card when round_index={round_index} and turn_index={turn_index}")

                # We don't allow requesting the trump card if the trump card is already shown:
                if self.game.trump_shown:
                    return try_play(feedback="trump suit already shown")

                # Trump request successful:
                return None

            else:
                # Remove the card from the player's hand:
                play_card = self.remove_card_from_hand(play_card_index)

                # Ensure the player's card is valid, given the other cards in their hand:
                if self.game.trump_shown and play_card.suit != self.game.trump_suit:
                    has_trump_suit_card = self.game.trump_suit in {card.suit for card in self.hand}
                    if has_trump_suit_card:
                        return try_play(feedback="card in trump suit available, but not played")

                # All okay, returning the played card:
                return play_card

        # try_play invokes and validates on_play repeatedly until a valid move is produced.
        return try_play()

    def retrieve_trump(self, card: Card):
        self.on_retrieve_trump(card)
        self.hand.append(card)

    @abstractmethod
    def on_bid(self) -> int:
        pass

    @abstractmethod
    def on_select_trump(self) -> int:
        pass

    @abstractmethod
    def on_play(self, round_index, turn_index, feedback=None) -> int:
        pass

    @abstractmethod
    def on_retrieve_trump(self, card: Card):
        pass

    #
    # Helper methods:
    #

    def remove_card_from_hand(self, card_index) -> Card:
        play_card = self.hand[card_index]
        self.hand = self.hand[:card_index] + self.hand[1+card_index:]
        return play_card


class Game(object):
    def __init__(self, player_count, start_player_index=0):
        self.players = [Player(self, f"player {i}") for i in range(1, 1+player_count)]
        self.start_player_index = start_player_index
        self.deck = generate_deck(player_count)
        self.trump_card = None
        self.trump_shown = False
        self.teams = [
            Team(self.players[0::2]),
            Team(self.players[1::2])
        ]

    @property
    def trump_suit(self):
        if self.trump_card:
            return self.trump_card.suit
        else:
            return None

    def start(self):
        def help_generate_deck(faces):
            return random.shuffle([
                Card(rank, suit)
                for rank in faces
                for suit in Card.Suit
            ])

        def generate_deck_6p():
            return help_generate_deck([
                Card.Face.Jack, Card.Face.Nine, Card.Face.Ten, Card.Face.Ace,
                Card.Face.Queen, Card.Face.King
            ])

        def generate_deck_4p():
            # Exclude the Queen and King
            return help_generate_deck([
                Card.Face.Jack, Card.Face.Nine, Card.Face.Ten, Card.Face.Ace,
            ])

        def generate_deck(player_count):
            if player_count == 4:
                generate_deck_4p()
            elif player_count == 6:
                generate_deck_6p()
            else:
                raise NotImplementedError()

        # Generating and dealing a deck of cards:
        deck = generate_deck(len(self.players))
        cards_per_player = len(deck) / len(self.players)
        for index, player in enumerate(self.players):
            offset = index * cards_per_player
            player.dealt(deck[offset:offset+cards_per_player])

        # Accepting bids from players, one-by-one, until N-1 players pass
        # consecutively:
        player_index = self.start_player_index
        consecutive_pass_ctr = 0
        highest_bidder = None
        highest_bidder_index = None
        highest_bid = 0

        # TODO: Currently implements N passes instead of N-1; verify.
        #       What if all N-1 players initially pass?
        while consecutive_pass_ctr < len(self.players):
            player = self.players[player_index]
            bid = player.bid(highest_bid)

            if bid:
                assert bid > highest_bid
                highest_bidder = player
                highest_bidder_index = player_index
                highest_bid = bid
                consecutive_pass_ctr = 0
            else:
                consecutive_pass_ctr += 1

            player_index = (1+player_index) % len(self.players)

        # Asking the highest bidder to select a trump card for the round:
        assert highest_bidder
        self.trump_card = highest_bidder.select_trump()

        # Running N rounds:
        round_count = 8
        round_starter_index = highest_bidder_index
        for round_index in range(0, round_count):
            logging.info(f"Beginning round {1+round_index}")
            round_cards = []
            total_round_points = 0
            winning_player_index = None
            winning_player = None
            winning_card = None
            round_suit = None

            # Playing a round, one per player:
            for turn_index in range(len(self.players)):
                player_index = (round_starter_index + turn_index) % len(self.players)
                player = self.players[player_index]
                played_card = player.play(round_index, turn_index)

                trump_requested = played_card is None
                if trump_requested:
                    assert not self.trump_shown
                    self.trump_shown = True
                    highest_bidder.retrieve_trump(self.trump_card)

                else:
                    if turn_index == 0:
                        winning_card = played_card
                        winning_player_index = player_index
                        winning_player = player
                        round_suit = played_card
                        # TODO: Update total_round_points
                    else:
                        # TODO: card_compare(winning_card, played_card, round_suit, self.trump_suit)
                        # TODO: update winning_card, winning_player_index
                        # TODO: Update total_round_points
                        pass

            # The winner of this round gets to start the next round:
            round_starter_index = winning_player_index

            # and pockets all the points for the elapsed round:
            assert winning_player
            winning_player.score += total_round_points

        # TODO: Determining which team won:


    # Run all 8 rounds of this, calling play_round for each.
    def play_all_rounds(self):
        round_starter_index = self.starting_player
        num_rounds = 0
        rounds = []
        while num_rounds < 8:
            num_rounds += 1
            logging.info("\nBeginning round {}".format(num_rounds))
            if self.trump_revealed:
                round = Round(trump_suit=self.trump_suit)
            else:
                round = Round()
            self.play_round(round, round_starter_index)
            round_starter_index = round.winning_player.number
            rounds.append(round)
            # logging.info("Round json: {}".format(round.json()))
            # pprint.pprint(round.json())
            # Let all players know what happened here
            for player in self.players:
                player.update_end_of_round_info(round)
            logging.info("Round {} won by {}, worth {} points".format(num_rounds, round.winning_player.name, round.round_pts))
        self.game_rounds = list(rounds)

    def play_round(self, round, start_index):
        turns = 0
        next_player = self.players[start_index]
        while turns < self.num_players:
            # logging.info("Object json: {}\n".format(self.json))
            self.play_turn(round, next_player)
            turns += 1
            next_player = self.players[(start_index + turns) % self.num_players]
            # print (self.json, end='\n****\n')
            # logging.info("Round json:\n{}".format(round.json()))
            # pprint.pprint(round.json())

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
                else: # idk do the request in a loop?? AI that makes a bad request might be uh something
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
        self.state = GameState.END_OF_GAME
        blue_pts, red_pts = 0, 0
        # Total the points
        for round in self.game_rounds:
            if round.winning_player.team == "BLUE":
                blue_pts += round.round_pts
            else:
                red_pts += round.round_pts
        logging.info("Blue pts: {} Red pts: {}".format(blue_pts, red_pts))
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

    # Whole game, bidding to round-play, to determining overall points
    def play_game(self):
        # self.generate_deck()
        # self.deal_to_players()
        # self.process_bidding_round()

        # TODO: Work on play_all_rounds:
        self.play_all_rounds()
        self.determine_game_points()
        self.reset_game()

    def old_init(self, num_players, strategies=None, randomize_start=False):
        assert num_players in [4, 6]
        logging.info("Starting game engine to play game with {} players".format(num_players))
        self.num_players = num_players
        self.player_hands = [[] for i in range(num_players)]
        self.state = GameState.INITIALIZED

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
        self.bid_history = []
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
            self.state = GameState.WAITING_FOR_PLAYERS
            # self.players = [None for i in range(self.num_players)]

