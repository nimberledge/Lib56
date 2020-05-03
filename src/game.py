"""
This module provides classes to encapsulate one ongoing game and its players.
"""

import random

from abc import ABCMeta, abstractmethod
from enum import Enum, auto as iota


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
    def __init__(self, players):
        super().__init__()
        self.players = players


class Player(object, metaclass=ABCMeta):
    def __init__(self, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.hand = []

    @abstractmethod
    def bid(self):
        pass

    @abstractmethod
    def select_trump(self):
        pass

    @abstractmethod
    def play(self):
        pass


class Game(object):
    def __init__(self, player_count):
        self.players = [Player(self, f"player {i}") for i in range(1, 1+player_count)]
        self.deck = generate_deck(player_count)
        self.trump_card = None
        self.trump_shown = False
        self.teams = [
            Team(self.players[0::2]),
            Team(self.players[1::2])
        ]

    def start(self):
        # TODO: Implement one full game for `self.players`.
        raise NotImplementedError()


def generate_deck(player_count):
    def help_generate_deck(faces):
        return random.shuffle([
            Card(rank, suit)
            for rank in faces
            for suit in Card.Suit
        ])

    def generate_deck_4p():
        return help_generate_deck([
            Card.Face.Jack, Card.Face.Nine, Card.Face.Ten, Card.Face.Ace,
        ])

    def generate_deck_6p():
        return help_generate_deck([
            Card.Face.Jack, Card.Face.Nine, Card.Face.Ten, Card.Face.Ace,
            Card.Face.Queen, Card.Face.King
        ])

    if player_count == 4:
        generate_deck_4p()
    elif player_count == 6:
        generate_deck_6p()
    else:
        raise NotImplementedError()


