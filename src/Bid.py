from Card import *
from PlayerStrategy import PlayerStrategy

class Bid(object):

    # bid_amount = 0 corresponds to passing
    def __init__(self, player, bid_amount):
        self.player = player
        self.bid_amount = bid_amount

    @cached_property
    def json(self):
        ret_dict = {}
        ret_dict['player'] = self.player.json
        ret_dict['bid_amount'] = self.bid_amount
        return json.dumps(ret_dict)
