"""
This class represents the route-cards of the game
"""

from .map.City import City


class RouteCard(object):

    def __init__(self, start: City, end: City, score: int):
        """
        Initializer for the route cards which takes three parameters
        :param start: start city of route
        :param end: end city of route
        :param score: score points for finishing this route
        """
        self.route_name = f'{start.name}-{end.name}'
        self.start = start
        self.end = end
        self.score = score
        self.shortest_routes = {}
        self.is_finished = False

    def set_finished(self):
        self.is_finished = True

    def add_shortest_route(self, agent_id, shortest_route):
        """
        Function that adds shortest route to the player card field
        :param agent_id: Agent for which the shortest route will be updated
        :param shortest_route: The actual shortest route that is added
        """
        self.shortest_routes[agent_id] = shortest_route

    def __str__(self):
        return f'{self.start}-{self.end}: {self.score}'
