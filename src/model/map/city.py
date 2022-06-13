"""
Object that represents a city
"""

class City(object):

    def __init__(self, name: str, coordinates: tuple):
        """
        Initializer of city object
        :param name: The name of the city
        :param coordinates: the coordinates of the city in float numbers
        """
        self.name = name
        self.coordinates = coordinates
        self.station = False
        self.station_owner = None
        # ?extra score points for specific cities?

    def __str__(self):
        return f'{self.name}: {self.coordinates}'
