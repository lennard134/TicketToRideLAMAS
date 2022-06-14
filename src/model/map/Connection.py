"""
Contains a start point and an end point of a connection, the color and number of trains, and the owner
"""

# packages
from src.model.map.City import City
from src.model import Agent


class Connection(object):

    def __init__(self, start: City, end: City, num_trains: int, color: str):
        """
        Initializer of a connection taking 4 parameters
        :param start: Start city of connection
        :param end: End city of connection
        :param num_trains: Number of trains that fit in the connection
        :param color: Color of the connection
        """
        self.start_point = start
        self.end_point = end
        self.num_trains = num_trains
        self.color = color
        self.owner = None

    def set_owner(self, agent: Agent):
        self.owner = agent
