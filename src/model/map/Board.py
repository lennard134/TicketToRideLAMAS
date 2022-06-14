"""
This class represents the board of the game
"""

# packages
from src.model.map.City import City
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# settings
CITY_FILE_PATH = os.path.join(ROOT_DIR, "data/cities.txt")


class Board(object):
    def __init__(self):
        self.cities = []
        self.connections = []

        self._init_cities()

    def _init_cities(self):
        """
        Function that initializes all cities
        Required: data in txt file with name and coordinates
        """
        with open(CITY_FILE_PATH, mode='r', encoding='utf-8') as f:
            for line in f:
                line_list = line.split()
                city_name = line_list[0]
                x_coord = float(line_list[1])
                y_coord = float(line_list[2])
                new_city = City(name=city_name, coordinates=(x_coord, y_coord))
                self.cities[city_name] = new_city

    def get_city(self, city_name: str):
        try:
            return self.cities[city_name]
        except KeyError:
            return None


if __name__ == "__main__":
    print(CITY_FILE_PATH)

