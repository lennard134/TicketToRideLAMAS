"""
This class represents the board of
"""

# packages
from .city import City


class Board(object):
    def __init__(self):
        self.cities = []
        self.connections = []
        self.cards = []

    def init_cities(self, file_path: str):
        """ Required: data in txt file with name and coordinates """
        with open(file_path, mode='r', encoding='utf-8') as f:
            for line in f:
                line_list = line.split()
                city_name = line_list[0]
                x_coord = float(line_list[1])
                y_coord = float(line_list[2])
                new_city = City(name=city_name, coordinates=(x_coord, y_coord))
                self.cities.append(new_city)

    def give_cards(self):
        pass


