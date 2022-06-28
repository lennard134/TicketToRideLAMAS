"""
Game object containing all relevant game-items for the player
"""

from .map.Board import Board
from .Deck import Deck
from .RouteCard import RouteCard
from .ttr_kripke.TtRKripke import TtRKripke
from .map.Connection import Connection
from .search_alg.Graph import Node, Graph


class Game(object):

    def __init__(self, board: Board, route_cards: dict[str: RouteCard], agent_list: list, deck: Deck, model: TtRKripke):
        """
        Initializer of game object
        :param board: Board object of the game
        :param route_cards: Different route cards
        :param agent_list: List of agents
        """
        self.route_cards = route_cards
        self.board = board
        self.agent_list = agent_list  # List with agent objects, not defined because of circular import
        self.deck = deck
        self.model = model
        self.graph = None

        self._init_graph()

    def init_shortest_routes(self):
        """
        Initial calculation of the shortest route for each route card for each agent
        """
        for route_card in self.route_cards.values():
            from_city = route_card.start.name
            target_city = route_card.end.name
            shortest_route = self.calculate_shortest_route(from_city, target_city, 0)
            for agent in self.agent_list:
                route_card.add_shortest_route(agent.agent_id, shortest_route=shortest_route)

    def calculate_shortest_route(self, from_city: str, target_city: str, agent_id: int):
        """
        Function to calculate the shortest route between two cities for an agent
        :param from_city: Start city of route card
        :param target_city: End city of route card
        :param agent_id: Agent for which the route is calculated
        :return: List with shortest route
        """
        self.graph.setup(from_city, target_city)
        self.update_graph_for_agent(agent_id)
        list_of_city_names = self.graph.get_shortest_route()
        if not list_of_city_names:
            return []

        shortest_route_list = []
        start = list_of_city_names[0]
        for end in list_of_city_names[1:]:
            shortest_route_list.append(self.board.get_connection(start, end))
            start = end

        return shortest_route_list

    def _init_graph(self):
        """
        Initialize graph for path planning
        """
        self.graph = Graph()

        # Add vertices
        for city_name in self.board.cities.keys():
            self.graph.add_node(Node(city_name))

        # Add edges
        for connection in self.board.connections:
            city1 = connection.start_point.name
            city2 = connection.end_point.name
            nr_trains = connection.num_trains

            self.graph.add_edge(city1, city2, nr_trains)

    def update_graph_for_agent(self, agent_id: int):
        """
        Function that updates the graph for an agent based on the claimed connections
        :param agent_id: Agent for which the graph has to be updated
        """
        for connection in self.board.connections:
            city1 = connection.start_point.name
            city2 = connection.end_point.name
            if connection.owner == agent_id:
                nr_trains = 0
            elif connection.owner is None:
                nr_trains = connection.num_trains
            else:  # connection has owner unequal to current agent
                continue

            self.graph.add_edge(city1, city2, nr_trains)

    def recalculate_shortest_routes(self):
        """
        Update the shortest routes based on changes on board
        """
        for route_card in self.route_cards.values():
            from_city = route_card.start.name
            target_city = route_card.end.name
            for agent in self.agent_list:  # List with agents
                shortest_route = self.calculate_shortest_route(from_city, target_city, agent.agent_id)
                route_card.add_shortest_route(agent.agent_id, shortest_route=shortest_route)

    def announce_claimed_connection(self, announcing_agent_id: int, claimed_connection: Connection):
        """
        Function updates Kripke model based on claimed connection by agent id
        :param announcing_agent_id: Agent that claims connection
        :param claimed_connection: Connection that is being claimed
        """
        # check if some agent now knows possible cards from agent_id
        for agent in self.agent_list:
            possible_singled_out = []
            if agent.agent_id != announcing_agent_id:
                for route_card in self.route_cards.values():
                    if route_card not in agent.own_route_cards and not route_card.is_finished:
                        if claimed_connection in route_card.shortest_routes[announcing_agent_id]:
                            possible_singled_out.append(route_card.route_name)
                route_to_update = set(possible_singled_out)
                self.model.update_possible_relations(agent_id=agent.agent_id, target_agent_id=announcing_agent_id,
                                                     route_cards=route_to_update)

        public_singled_out = set([])
        for route_card in self.route_cards.values():
            # only in one route_card
            if claimed_connection in route_card.shortest_routes[announcing_agent_id] and not route_card.is_finished:
                public_singled_out.add(route_card.route_name)

        # possibilities
        self.model.public_announcement_possibilities(announcing_agent_id, public_singled_out)
