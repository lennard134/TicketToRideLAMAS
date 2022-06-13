"""
Contains a start point and an end point of a connection, the color and number of trains, and the owner
"""

class Connection(object):

    def __init__(self, start: str, end: str, num_trains: int, color: str):
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