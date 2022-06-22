"""
This class represents the board of the game
"""

# packages
from src.model.map.City import City
from src.model.map.Connection import Connection
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# settings
CITY_FILE_PATH = os.path.join(ROOT_DIR, "data/cities.txt")
CONNECTION_FILE_PATH = os.path.join(ROOT_DIR, "data/train_routes_all.txt")


class Board(object):

    def __init__(self):
        """
        Initializer for board, no parameters are given
        """
        self.cities = {}
        self.connections = []
        self.adjacency_list = {}  # city_name -> [list of connections]

        self._init_cities()
        self._init_connections()
        self._make_adjacency_list()  # MUST BE AFTER CONNECTIONS TODO: Needed???

    def _make_adjacency_list(self):
        for city_name in self.cities.keys():
            self.adjacency_list[city_name] = []

        for connection in self.connections:  # {"routeX": [a:Connection,b:Connection,c,f]}
            from_city = connection.start_point.name
            to_city = connection.end_point.name
            self.adjacency_list[from_city].append(connection)
            self.adjacency_list[to_city].append(connection)

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

    def _init_connections(self):
        """
        Read connections from text file and create new Connection objects for every city on the map
        """
        with open(CONNECTION_FILE_PATH, mode='r', encoding='utf-8') as f:
            for line in f:
                line_list = line.split()
                start = self.get_city(line_list[0].split('-')[0])
                end = self.get_city(line_list[0].split('-')[1])

                if start is None or end is None:
                    print(f'Cities {start} or {end} not implemented. Skipping connection....')
                    continue

                length = int(line_list[1].rpartition('(')[2].partition(')')[0])
                color = line_list[3]

                self.connections.append(Connection(start, end, length, color))

    def get_city(self, city_name: str):
        try:
            return self.cities[city_name]
        except KeyError:
            return None


if __name__ == "__main__":
    print(CITY_FILE_PATH)

