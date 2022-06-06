class Connection(object):
    """Contains a start point and an end point of a connection, the color and number of trains, and the owner"""

    def __init__(self, start: str, end: str, num_trains: int, color: str):
        self.start_point = start
        self.end_point = end
        self.num_trains = num_trains
        self.color = color
        self.owner = None
