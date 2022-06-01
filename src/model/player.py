class Player(object):

    def __init__(self, player_id):
        self.player_id = player_id
        self.route_cards = []
        self.owned_connections = []
        self.train_cards = []
