"""
This class represents the route-cards of the game
"""
class RouteCard(object):

    def __init__(self, start: str, end: str, score: int):
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
        self._owner = None
        self.finished_card = False

    def set_owner(self, agent: Agent):
        self._owner = agent

    def get_owner(self):
        return self._owner if self.finished_card else None

    def set_finished(self):
        self.finished_card = True

    def add_shortest_route(self, agent_id, shortest_route):
        self.shortest_routes[agent_id] = shortest_route

    def __str__(self):
        return f'{self.start}-{self.end}: {self.score}'
