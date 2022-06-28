"""
This class represents the board of the game
"""

# packages
from src.model.map.City import City
from src.model.map.Connection import Connection, FerryConnection
from src.model.Deck import TRAIN_COLOURS
from src.model import config

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# settings
CITY_FILE_PATH = os.path.join(ROOT_DIR, config.BOARD_CONFIG['CITY_FILE_PATH'])
CONNECTION_FILE_PATH = os.path.join(ROOT_DIR, config.BOARD_CONFIG['CONNECTION_FILE_PATH'])
GRAY_CONNECTION = config.BOARD_CONFIG['GRAY_COLOUR']


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
        """
        Function that creates adjacency list for all cities
        """
        for city_name in self.cities.keys():
            self.adjacency_list[city_name] = []

        for connection in self.connections:  # {"routeX": [a:Connection,b:Connection,c,f]}
            from_city = connection.start_point.name
            to_city = connection.end_point.name
            self.adjacency_list[from_city].append(connection)
            self.adjacency_list[to_city].append(connection)

    def get_connection(self, city1: str, city2: str):
        list_of_connections = self.adjacency_list[city1]
        for connection in list_of_connections:
            if connection.end_point.name == city2 or connection.start_point.name == city2:
                return connection
        return None

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
                city1 = self.get_city(line_list[0].split('-')[0])
                city2 = self.get_city(line_list[0].split('-')[1])

                if city1 is None or city2 is None:
                    # print(f'Cities {city1} or {city2} not implemented. Skipping connection....')
                    continue

                length = int(line_list[1].rpartition('(')[2].partition(')')[0])
                color = line_list[3]

                is_new = True
                for connection in self.connections:
                    city1_old = connection.start_point.name
                    city2_old = connection.end_point.name
                    if (city1_old == city1.name and city2_old == city2.name) or (city1_old == city2.name and city2_old == city1.name):
                        is_new = False
                        print(f"Connection {city1_old}-{city2_old} is double")
                        break

                if is_new:
                    if color not in TRAIN_COLOURS and not color == GRAY_CONNECTION:
                        num_jokers = int(color)
                        self.connections.append(FerryConnection(city1, city2, length, color, num_jokers))
                    else:
                        self.connections.append(Connection(city1, city2, length, color))

    def get_city(self, city_name: str):
        try:
            return self.cities[city_name]
        except KeyError:
            return None
