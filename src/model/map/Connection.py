"""
Contains a start point and an end point of a connection, the color and number of trains, and the owner
"""

# packages
from src.model.map.City import City


class Connection(object):

    def __init__(self, start: City, end: City, num_trains: int, color: str):
        """
        Initializer of a connection taking 4 parameters
        :param start: Start city of connection
        :param end: End city of connection
        :param num_trains: Number of trains that fit in the connection
        :param color: Color of the connection
        :param owner: Agent that owns the connection
        """
        self.start_point = start
        self.end_point = end
        self.connection_name = f'{self.start_point.name}-{self.end_point.name}'
        self.num_trains = num_trains
        self.color = color
        self.owner = None

    def set_owner(self, agent_id: int):
        self.owner = agent_id


class FerryConnection(Connection):

    def __init__(self, start: City, end: City, num_trains: int, color: str, num_jokers: int):
        """
        Sub class of connection to represent ferry connection, class is almost same as connection, only number of
        jokers is added
        :param start: Start city of ferry connection
        :param end: End city of ferry connection
        :param num_trains: Number of trains necessary excluding jokers
        :param color: Color to represent the connection
        :param num_jokers: Number of jokers necessary to claim this connection
        """
        super().__init__(start, end, num_trains, "gray")
        self.num_jokers = num_jokers

