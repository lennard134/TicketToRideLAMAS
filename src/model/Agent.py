"""
Object player that holds all information necessary for an agent to play the game
"""

# settings
from .Game import Game
from .RouteCard import RouteCard
from .map.Connection import Connection, FerryConnection
from .Deck import TRAIN_COLOURS
from .config import *

import numpy as np

# Params in Agent Config
START_SCORE = AGENT_CONFIG['START_SCORE']
JOKER_COLOUR = DECK_CONFIG['JOKER_COLOUR']
NR_CARDS_TO_DRAW = AGENT_CONFIG['NR_CARDS_TO_DRAW']
GRAY_CONNECTION = BOARD_CONFIG['GRAY_COLOUR']
TRAIN_POINTS = BOARD_CONFIG['TRAIN_POINTS']


class Agent(object):

    def __init__(self, agent_id: int, nr_of_trains: int, game: Game = None):
        """
        Initializer for object player.
        :param agent_id: Id of the agent
        :param nr_of_trains: Number of trains that a player can use to claim routes
        """
        self.score = START_SCORE
        self.agent_id = agent_id
        self.nr_of_trains = nr_of_trains
        self.game = game
        self.hand = []
        self.own_route_cards = []
        self.can_draw_card = True
        self.last_move = ''

    def get_route_cards_str(self):
        route_cards = []
        for route_card in self.own_route_cards:
            route_cards.append(route_card.route_name)
        return route_cards

    def place_trains(self, nr_trains: int) -> bool:
        """
        Return true and removes trains if enough, else return false.
        """
        if nr_trains > self.nr_of_trains:
            return False
        self.nr_of_trains -= nr_trains
        self.score += TRAIN_POINTS[nr_trains]
        return True

    def set_game(self, game: Game):
        self.game = game

    def select_connection_to_claim(self, claimable_connections: list[Connection]) -> Connection:
        """
        Function that determines which connection should be claimed based on the score of the routes
        :param claimable_connections: Possible connections an agent can claim
        :return: The connection an agent should claim
        """
        connection_value = [0] * len(claimable_connections)

        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                if connection in claimable_connections:
                    index_connection = claimable_connections.index(connection)
                    connection_value[index_connection] = max(route_card.score, connection_value[index_connection])
        return claimable_connections[np.argmax(connection_value)]

    def print_agent_profile(self):
        """
        Function to print profile of the agent showing the owned train cards, number of trains, owned connections
        and which states this agent considers.
        """
        print(f"\n------\nProfile agent {self.agent_id}:")
        print(f"* Owned train cards: {self.hand}")
        print(f"* Number of trains: {self.nr_of_trains}")
        print(f"* Owned connections:")
        for connection in self.game.board.connections:
            if connection.owner == self.agent_id:
                print(f"* -- {connection.connection_name}")
        print(f"* Considered states:")
        for state in self.game.model.worlds:
            if state.has_agent_in_agent_list(self.agent_id, self.agent_id):
                print(f"* -- {str(state)}")
        print(f"------\n")

    def check_route_finished(self, route_card: RouteCard) -> bool:
        """
        Checks if an unfinished route card has been finished and sets the card to finished if so.
        :param route_card: RouteCard that is evaluated
        :return: boolean True if route finished else False
        """
        shortest_route = route_card.shortest_routes[self.agent_id]
        if not shortest_route:
            # shortest route is empty, so does not exist
            return False

        for connection in shortest_route:
            if not connection.owner == self.agent_id:
                return False

        return True

    def check_if_route_cards_done(self) -> bool:
        """
        Check if player has finished all route cards
        :return: True if player finished all cards, else False
        """
        for route_card in self.own_route_cards:
            if not route_card.is_finished:
                return False
        return True

    def check_block_connection(self) -> dict[int]:
        """
        Function to check if it is possible for an agent to block another agent
        :return: Dictionary with possible connections to block
        """
        possible_blocks = {}
        for agent in self.game.agent_list:
            if not agent.agent_id == self.agent_id:
                known_routes_str = self.game.model.get_known_route_cards(self.agent_id, agent.agent_id)
                for known_route_str in known_routes_str:
                    blockable_connections = self.game.route_cards[known_route_str].shortest_routes[agent.agent_id]
                    for connection in blockable_connections:
                        if connection.owner is None and self.enough_cards_to_claim_train_card(connection):
                            if agent in possible_blocks.keys():
                                possible_blocks[agent.agent_id].extend((known_route_str, connection))
                            else:
                                possible_blocks[agent.agent_id] = [(known_route_str, connection)]

        return possible_blocks

    def block_connection(self, agent_id_blocked, block_tuple: tuple[str, Connection]):
        """
        Function that blocks a connection and does public announcement of the connection and owner
        :param agent_id_blocked: Id of agent of which a connection will blocked
        :param block_tuple: Tuple containing route card and a connection
        """
        route_card, connection = block_tuple
        self.game.model.public_announcement_route_card(agent_id_blocked, {route_card})
        self.claim_connection(connection, 'block')

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
                drawn_closed_card = self.game.deck.remove_closed_card()
                if drawn_closed_card is None:
                    self.can_draw_card = False
                else:
                    self.hand.append(drawn_closed_card)

    def get_desired_colours(self) -> list:
        """
        Determine the desired colours based on the potential connections to claim
        :return: list of desired coloured
        """
        desired_cards_count = {}
        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                needed_cards = connection.num_trains - self.hand.count(connection.color)
                if connection.color in desired_cards_count.keys():
                    desired_cards_count[connection.color] = min(desired_cards_count[connection.color], needed_cards)
                else:
                    desired_cards_count[connection.color] = needed_cards

        ordered_desired_cards_count = dict(sorted(desired_cards_count.items(), key=lambda item: item[1]))

        desired_cards = []
        for color, count in ordered_desired_cards_count.items():
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

    def enough_cards_to_claim_train_card(self, connection):
        """
        Returns True if agent has sufficient hand to claim connection, else returns False
        """
        if connection.color == GRAY_CONNECTION:
            for color in TRAIN_COLOURS:
                enough_train_cards = connection.num_trains <= self.hand.count(color) + self.hand.count(JOKER_COLOUR)
                if isinstance(connection, FerryConnection):
                    enough_jokers = connection.num_jokers <= self.hand.count(JOKER_COLOUR)
                    enough_train_cards = connection.num_trains <= self.hand.count(color) + self.hand.count(JOKER_COLOUR)
                    enough_train_cards = enough_train_cards and enough_jokers
                if enough_train_cards:
                    return True
        return connection.num_trains <= self.hand.count(connection.color) + self.hand.count(JOKER_COLOUR)

    def check_claim_connection(self) -> list:
        """
        If it can claim, mark connection as claimable
        :return: True if connection is claimed else False
        """
        claimable_connections = []
        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                if connection.owner is None and self.enough_cards_to_claim_train_card(connection) \
                        and self.nr_of_trains >= connection.num_trains:
                    claimable_connections.append(connection)

        return claimable_connections

    def claim_connection(self, connection: Connection, claim_type='claim'):
        """
        Agent claims a connection by putting trains on a connection
        """
        print(f"-- Agent {self.agent_id} {claim_type}s connection {connection.end_point.name}-{connection.start_point.name}"
              f" with color {connection.color} and costs {connection.num_trains}.")

        connection.set_owner(self.agent_id)
        connection_color = connection.color

        if connection_color == GRAY_CONNECTION:
            max_color_count = (TRAIN_COLOURS[0], self.hand.count(TRAIN_COLOURS[0]))
            for color in TRAIN_COLOURS[1:]:
                _, count = max_color_count
                if count < self.hand.count(color):
                    max_color_count = (color, self.hand.count(color))
            connection_color, _ = max_color_count

        if isinstance(connection, FerryConnection):
            color_count = min(self.hand.count(connection_color), connection.num_trains - connection.num_jokers)
        else:
            color_count = min(self.hand.count(connection_color), connection.num_trains)
        joker_count = connection.num_trains - color_count

        color_list = [connection_color] * color_count + [JOKER_COLOUR] * joker_count
        self.game.deck.play_train_cards(color_list)
        self.place_trains(connection.num_trains)

        for color in color_list:
            self.hand.remove(color)

        if claim_type == 'claim':
            self.game.announce_claimed_connection(self.agent_id, connection)

        self.game.recalculate_shortest_routes()

        for route_card in self.own_route_cards:
            if not route_card.is_finished and self.check_route_finished(route_card):
                self.score += route_card.score  # Add score from finished route card
                print(f"\n### Agent {self.agent_id} finished route card {route_card.route_name} with "
                      f"{route_card.score} points! ###\n")
                self.game.model.public_announcement_route_card(agent_id=self.agent_id,
                                                               route_card={route_card.route_name})
                route_card.set_finished()

    def choose_action(self):
        """
        By default, every agent chooses to claim a connection advancing its own route cards. However, when it knows a
        route card of another agent (and this has been publicly announced) they will choose to block said route.
        """
        self.can_draw_card = True

        # Greedy implementation
        claimable_connections = self.check_claim_connection()
        if claimable_connections:
            print(f"- Agent {self.agent_id} claims connection.")
            claimed_connection = self.select_connection_to_claim(claimable_connections)
            self.claim_connection(claimed_connection, 'claim')
            self.last_move = f'claims {claimed_connection.connection_name}'
        else:
            claimable_connections = self.check_block_connection()
            if claimable_connections:

                print(f"- Agent {self.agent_id} blocks connection.")
                agent_to_block = np.random.choice(list(claimable_connections.keys()))
                block_tuple_idx = np.random.choice(range(len(claimable_connections[agent_to_block])))
                block_tuple = claimable_connections[agent_to_block][block_tuple_idx]
                self.block_connection(agent_to_block, block_tuple)
                self.last_move = f'blocks agent {agent_to_block}: {block_tuple[1].connection_name}'
            else:
                print(f"- Agent {self.agent_id} draws card.")
                self.draw_card()
                self.last_move = f'draws card'
        print()

    def __str__(self):
        return f"Agent {self.agent_id}. "
