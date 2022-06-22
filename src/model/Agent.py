"""
Object player that holds all information necessary for an agent to play the game
"""

# settings
from src.model.Game import Game
from src.model.RouteCard import RouteCard
from src.model.map.Connection import Connection

import numpy as np

START_SCORE = 0
JOKER_COLOUR = "joker"
NR_CARDS_TO_DRAW = 2


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

    def place_trains(self, nr_trains: int) -> bool:
        """
        Return true and removes trains if enough, else return false.
        """
        if nr_trains > self.nr_of_trains:
            return False
        self.nr_of_trains -= nr_trains
        return True

    def set_game(self, game: Game):
        self.game = game

    def select_connection_to_claim(self, claimable_connections: list[Connection]) -> Connection:
        """
        Function that determines which connection should be claimed based on the score of the routes
        :param claimable_connections: Possible connections an agent can claim
        :return: The connection an agent should claim
        """
        # TODO: gooi dit in een andere functie waarin we de claimable connecties maken???
        connection_value = [0] * len(claimable_connections)

        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                if connection in claimable_connections:
                    index_connection = claimable_connections.index(connection)
                    connection_value[index_connection] = max(route_card.score, connection_value[index_connection])
        return claimable_connections[np.argmax(connection_value)]

    def choose_action(self):
        """
        By default, every agent chooses to claim a connection advancing its own route cards. However, when it knows a
        route card of another agent (and this has been publicly announced) they will choose to block said route.
        """

        # TODO: determine if other routes known
        #       check for possible routes that can be made with previous move and determine if one could be singled out

        # Greedy implementation
        claimable_connections = self.check_claim_connection()
        if claimable_connections:
            print(f"- Agent {self.agent_id} claims connection.")
            self.claim_connection(self.select_connection_to_claim(claimable_connections))
        else:
            claimable_connections = self.check_block_connection()
            if claimable_connections:
                print(f"- Agent {self.agent_id} blocks connection.")
                agent_to_block = np.random.choice(list(claimable_connections.keys()))
                block_tuple = np.random.choice(claimable_connections[agent_to_block])
                self.block_connection(agent_to_block, block_tuple)  # block tuple : (route_card: str, connection)
            else:
                print(f"- Agent {self.agent_id} draws card.")
                self.draw_card()

    def check_claim_connection(self) -> list:
        """
        If it can claim, directly claim the connection here
        :return: True if connection is claimed else False
        """
        claimable_connections = []
        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                # for connection in shortest_route:
                if connection.num_trains <= self.hand.count(connection.color) + self.hand.count(JOKER_COLOUR):
                    claimable_connections.append(connection)
                # else:
                #     print(f"hand not sufficient for connection, needed {connection.num_trains} times {connection.color}")
                    # print(self.hand)

        return claimable_connections

    def check_route_finished(self, route_card: RouteCard) -> bool:
        """
        Checks if an unfinished route card has been finished and sets the card to finished if so.
        """
        for connection in route_card.shortest_routes[self.agent_id]:
            if not connection.owner == self.agent_id:
                return False

        return True

    def check_if_done(self) -> bool:
        """
        Check if player has finished all route cards
        :return: True if player finished all cards, else False
        """
        for route_card in self.own_route_cards:
            if not route_card.is_finished:
                return False
        return True

    def check_block_connection(self) -> dict:
        """
        Function to check if it is possible for an agent to block another agent
        :return: Dictionary with possible connections to block
        """
        possible_blocks = {}  # dictionary with agent -> list of tuples (route, connection to block)
        for agent in self.game.agent_list:
            if not agent.agent_id == self.agent_id:
                known_routes_str = self.game.model.get_known_route_cards(self.agent_id, agent.agent_id)  # (list of strings)
                for known_route_str in known_routes_str:
                    blockable_connections = self.game.route_cards[known_route_str].shortest_routes[agent.agent_id]
                    for connection in blockable_connections:
                        if connection.color in self.hand and connection.num_trains <= self.hand.count(connection.color):
                            if agent in possible_blocks.keys():
                                possible_blocks[agent].extend((known_route_str, connection))
                            else:
                                possible_blocks[agent] = [(known_route_str, connection)]

        return possible_blocks

    def block_connection(self, agent_id_blocked, block_tuple: tuple[str, Connection]):
        """
        Function that blocks a connection and does public announcement of the connection and owner
        :param agent_id_blocked: Id of agent of which a connection will blocked
        :param block_tuple: Tuple containing route card and a connection
        """
        route_card, connection = block_tuple
        self.game.model.public_announcement_route_card(agent_id_blocked, route_card)
        self.claim_connection(connection)

    def claim_connection(self, connection: Connection):
        """
        Agent claims a connection by putting trains on a connection
        """
        print(f"- Agent {self.agent_id} claims connection {connection.end_point.name}-{connection.start_point.name}.")

        if connection.owner is not None:
            print(f"- this connection has already an owner {connection.owner}. EXITING....")
            
        connection.set_owner(self.agent_id)
        # TODO: gray color not included
        color_count = min(self.hand.count(connection.color), connection.num_trains)
        joker_count = connection.num_trains - color_count
        color_list = [connection.color] * color_count + [JOKER_COLOUR] * joker_count
        self.game.deck.play_train_cards(color_list)

        for color in color_list:
            self.hand.remove(color)

        self.game.announce_connection(self.agent_id, connection)

        for route_card in self.own_route_cards:
            if not route_card.is_finished and self.check_route_finished(route_card):
                # TODO: possibly make more efficient by using claimed connection
                route_card.set_finished()
                self.game.model.public_announcement_route_card(agent_id=self.agent_id, route_card=route_card.route_name)
                self.check_if_done()

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
                    else:
                        break

            if not card_drawn:
                self.hand.append(self.game.deck.remove_closed_card())

    def get_desired_colours(self) -> list:
        """
        Determine the desired colours based on the potential connections to claim
        :return: list of desired coloured
        """
        desired_cards_count = {}
        for route_card in self.own_route_cards:
            for connection in route_card.shortest_routes[self.agent_id]:
                if connection.color in self.hand:
                    desired_cards_count[connection.color] = connection.num_trains - self.hand.count(connection.color)

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

    def __str__(self):
        return f"Agent {self.agent_id}. "
               # f"Has route cards {[card for ]}"