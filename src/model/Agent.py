"""
Object player that holds all information necessary for an agent to play the game
"""

# settings
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
        self.hand = []
        self.own_route_cards = []
        self.owned_connections = []
        self.possible_route_cards = []

    def place_trains(self, nr_trains: int):
        """
        Return true and removes trains if enough, else return false.
        """
        if nr_trains > self.nr_of_trains:
            return False
        self.nr_of_trains -= nr_trains
        return True

    def choose_action(self):
        """
        Either put train on connection or get new cards from open/closed deck
        """
        pass

    def claim_connection(self):
        """
        Agent claims a connection by putting trains on a connection
        """
        pass

    def draw_card(self):
        """
        Agent can draw a card either open or closed, choice is made in this function if player draws open/closed card.
        """
        pass

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