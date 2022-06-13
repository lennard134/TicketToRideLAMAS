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
        self.start = start
        self.end = end
        self.score = score
        #? self.finished_card = false? Maybe finished if route is fully claimed by agent

    def __str__(self):
        return f'{self.start}-{self.end}: {self.score}'
