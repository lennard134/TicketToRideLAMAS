"""
Game object containing all relevant game-items for the player
"""

from src.model.map.Board import Board
from src.model.Deck import Deck
from src.model.RouteCard import RouteCard


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

    def init_shortest_routes(self):
        """
        Initial calculation of the shortest route for each route card for each agent
        """
        for route_card in self.route_cards:
            # calculate optimal routes
            shortest_route = None
            # just do it ✔
            for agent in self.agent_list:
                route_card.add_shortest_route(agent.agent_id, shortest_route=shortest_route)

    def recalculate_shortest_routes(self):
        """
        Update the shortest routes based on changes on board
        """
        for route_card in self.route_cards:
            for agent in self.agent_list:
                shortest_route = None
                route_card.add_shortest_route(agent.agent_id, shortest_route=shortest_route)

