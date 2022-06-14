"""
Object player that holds all information necessary for an agent to play the game
"""

# settings
from src.model.Game import Game
from src.model.RouteCard import RouteCard

START_SCORE = 0


class Agent(object):
    def __init__(self, agent_id: int, nr_of_trains: int):
        """
        Initializer for object player.
        :param agent_id: Id of the agent
        :param nr_of_trains: Number of trains that a player can use to claim routes
        """
        self.score = START_SCORE
        self.agent_id = agent_id
        self.nr_of_trains = nr_of_trains
        self.game = None
        self.hand = []
        self.own_route_cards = []
        self.owned_connections = []
        self.possible_route_cards = []
        self._shortest_paths = {}

    def place_trains(self, nr_trains: int):
        """
        Return true and removes trains if enough, else return false.
        """
        if nr_trains > self.nr_of_trains:
            return False
        self.nr_of_trains -= nr_trains
        return True

    def set_game(self, game: Game):
        self.game = game

    def choose_action(self):
        """
        Either put train on connection or get new cards from open/closed deck
        """
        self._recalculate_own_shortest_routes()

        # Greedy implementation
        if self.check_claim_connection():
            self.game.recalculate_shortest_routes()
        elif self.check_block_connection():
            self.game.recalculate_shortest_routes()
        else:
            self.draw_card()

    def check_claim_connection(self):
        """
        If it can claim, directly claim the connection here
        :return: True if connection is claimed else False
        """
        # Claim one of the connections of the shortest routes

        # If not possible, check if a connection that can be claimed can be part of new shortest route
        return False

    def check_block_connection(self):
        """
        If it can block another agent by claiming a connection it will do so directly
        :return: True if connection is claimed else False
        """
        return False

    def claim_connection(self):
        """
        Agent claims a connection by putting trains on a connection
        """
        pass

    def draw_card(self):
        """
        Agent can draw a card either open or closed, choice is made in this function if player draws open/closed card.
        """
        # From desired colours
        # either two closed cards, one open and one closed or two open, OR a single joker card from open
        desired_colours = self.get_desired_colours()

        if JOKER_COLOUR in self.game.deck.open_cards:
            self.game.deck.remove_open_card(JOKER_COLOUR)
            self.hand.append(JOKER_COLOUR)
            return

        for idx in range(NR_CARDS_TO_DRAW):
            card_drawn = False

            for colour in desired_colours:  # NO JOKER IN DESIRED COLOURS!!!
                if colour in self.game.deck.open_cards:
                    self.game.deck.remove_open_card(colour)
                    self.hand.append(colour)
                    card_drawn = True
                    if idx != NR_CARDS_TO_DRAW - 1:  # One less calculation of the desired colours
                        desired_colours = self.get_desired_colours()
                    break
            if not card_drawn:
                self.hand.append(self.game.deck.remove_closed_card())

    def get_desired_colours(self):
        """
        Determine the desired colours based on the potential connections to claim
        :return: list of desired coloured
        """
        return []

    def add_train_card(self, colour: str):
        """
        Give an agent a card of a colour 'colour'
        """
        self.hand.append(colour)

    def add_route_card(self, route_card: RouteCard):
        """
        Give an agent a route card
        """
        self.own_route_cards.append(route_card)

    def _recalculate_own_shortest_routes(self):
        """
        Shortest paths based on train cards you have
        """
        # add desired colours
        for route_card in self.own_route_cards:
            self._shortest_paths[route_card.route_name] = None

    def __str__(self):
        return f"Agent {self.agent_id}. "
               # f"Has route cards {[card for ]}"