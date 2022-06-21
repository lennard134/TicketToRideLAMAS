"""
Object player that holds all information necessary for an agent to play the game
"""

# settings
from src.model.Game import Game
from src.model.RouteCard import RouteCard
from src.model.map.Connection import Connection
from src.model.TtRKripke.TtRKripke import TtRKripke

import numpy as np

START_SCORE = 0
JOKER_COLOUR = "joker"
NR_CARDS_TO_DRAW = 2


class Agent(object):

    def __init__(self, agent_id: int, nr_of_trains: int, model: TtRKripke):
        """
        Initializer for object player.
        :param agent_id: Id of the agent
        :param nr_of_trains: Number of trains that a player can use to claim routes
        """
        self.score = START_SCORE
        self.agent_id = agent_id
        self.nr_of_trains = nr_of_trains
        self.model = model
        self.game = None
        self.current_working_route = None  # index of route agent is working on TODO: THIS STILL NEEDS TO BE IMPLEMENTED, UPDATED AND FIXED
        self.hand = []
        self.own_route_cards = []
        self.possible_route_cards = []
        self._shortest_paths = {}  # Key is route card name, value is list of tuples TODO: HWY IS THIS HERE??

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
        By default, every agent chooses to claim a connection advancing its own route cards. However, when it knows a
        route card of another agent (and this has been publicly announced) they will choose to block said route.
        """
        self._recalculate_own_shortest_routes()

        # TODO: determine if other routes known
        #       check for possible routes that can be made with previous move and determine if one could be singled out

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
        # {"routeX": [a,b,c,f]}
        claimable = []
        for route_card in self.own_route_cards:
            for shortest_route in route_card.shortest_routes[self.agent_id]:
                for connection in shortest_route:
                    if connection.color in self.hand and connection.num_trains <= self.hand.count(connection.color):
                        claimable.append(connection)

        # Claim one of the connections of the shortest routes
        if len(claimable) == 0:
            return False
        else:
            claimed_connection = np.random.choice(claimable)
            self.claim_connection(claimed_connection)
            self.game.update_previous_turn(agent_id=self.agent_id, connection=claimed_connection)

            for route_card in self.own_route_cards:
                if not route_card.is_finished and self.check_route_finished(route_card):
                    self.model.public_announcement_route_card(agent_id=self.agent_id, route_card=route_card)
                    self.check_if_done()
                    break

            return True

    def check_route_finished(self, route_card: RouteCard):
        """
        Checks if an unfinished route card has been finished and sets the card to finished if so.
        """
        for connection in route_card.shortest_routes[self.agent_id]:
            if not connection.owner == self.agent_id:
                return False

        # TODO: get new working route
        route_card.set_finished()
        return True

    def check_if_done(self):
        """
        Check if player has finished all route cards
        :return: True if player finished all cards, else False
        """
        for route_card in self.own_route_cards:
            if not route_card.is_finished:
                return False
        return True

    def check_block_connection(self):
        """
        If it can block another agent by claiming a connection it will do so directly and do a public announcement
        :return: True if connection is claimed else False
        """
        # for every opponent
        # check possible routes based on last move
        possible_opponent_routes = {}
        for agent, turn in self.game.get_previous_turn().items():
            if agent != self.agent_id:
                for route_card in self.possible_route_cards:
                    if not route_card.is_finished and route_card not in self.own_route_cards and \
                            turn in route_card.shortest_routes[agent]:
                        if agent in possible_opponent_routes.keys():
                            possible_opponent_routes[agent].extend(route_card)
                        else:
                            possible_opponent_routes[agent] = [route_card]

        for agent, route_cards in possible_opponent_routes:
            for route_card in route_cards:
                for connection in route_card:
                    

        # for possible routes, check if more connections of fastest route are filled
        # if one route singled out --> public announcement and block if block is possible
        # if more routes but all other from own routes --> public announcement and block if possible (else zip it)

        return False

    def claim_connection(self, connection: Connection):
        """
        Agent claims a connection by putting trains on a connection
        """
        connection.set_owner(self.agent_id)
        self.game.deck.play_train_cards([connection.color] * connection.num_trains)
        return True

    def draw_card(self):
        """
        Agent can draw a card either open or closed, choice is made in this function if player draws open/closed card.
        TODO: strategy for drawing cards should be refined down the line
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
        desired_cards_count = {}
        for connection in self.own_route_cards[self.current_working_route].shortest_routes:
            if connection.color in self.hand:
                desired_cards_count[connection.color] = connection.num_trains - self.hand.count(connection.color)

        ordered_desired_cards_count = dict(sorted(desired_cards_count.items(), key=lambda item: item[1]))

        desired_cards = []

        for color, count in ordered_desired_cards_count:
            desired_cards.extend([color] * count)

        return desired_cards

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