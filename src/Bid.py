from Card import *
from PlayerStrategy import PlayerStrategy

class Bid(object):

    # bid_amount = 0 corresponds to passing
    def __init__(self, player, bid_amount):
        self.player = player
        self.bid_amount = bid_amount
