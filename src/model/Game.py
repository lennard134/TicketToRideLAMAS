"""
Game object containing all relevant game-items for the player
"""

from src.model.map.Board import Board
from src.model.Deck import Deck
from src.model.RouteCard import RouteCard
from src.model.TtRKripke.TtRKripke import TtRKripke
from src.model.map.Connection import Connection
from src.model.search_alg.graph import Node, Graph


class Game(object):

    def __init__(self, board: Board, route_cards: list[RouteCard], agent_list: list, deck: Deck):
        """
        Initializer of game object
        :param board: Board object of the game
        :param route_cards: Different route cards
        :param agent_list: List of agents
        """
        self.route_cards = route_cards
        self.board = board
        self.agent_list = agent_list
        self.deck = deck
        self.previous_turns = {}

    def _init_shortest_routes(self):
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
        self.graph.setup(from_city, target_city)
        self.remake_graph_for_agent(agent_id)
        return self.graph.get_shortest_route()

    def recalculate_shortest_routes(self):
        """
        Update the shortest routes based on changes on board
        """
        for route_card in self.route_cards.values():
            from_city = route_card.start
            target_city = route_card.end
            for agent in self.agent_list:  # List with agents
                shortest_route = self.calculate_shortest_route(from_city, target_city, agent.agent_id)
                route_card.add_shortest_route(agent.agent_id, shortest_route=shortest_route)

    def announce_connection(self, agent_id: int, connection: Connection):

        # check if some agent now knows a card from agent_id
        # Recalculate shortest route
        self.recalculate_shortest_routes()

        #
        pass
