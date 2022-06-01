class Connection(object):
    """Contains a begin and end point of a connection, the color and number of trains, and the owner"""

    def __init__(self, begin: str, end: str, num_trains: int, color: str):
        self.begin_point = begin
        self.end_point = end
        self.num_trains = num_trains
        self.color = color
        self.owner = None
