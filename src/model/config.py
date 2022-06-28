"""
Config file containing settings for different classes in the form of a dictionary
"""

AGENT_CONFIG = {
    'START_SCORE': 0,
    'NR_CARDS_TO_DRAW': 2
}

DECK_CONFIG = {
    'NR_COLOUR_CARDS': 12,
    'NR_JOKERS': 14,
    'NR_OPEN_CARDS': 5,
    'TRAIN_COLOURS': [
        'red', 'pink', 'white', 'yellow', 'green', 'blue', 'black', 'orange'
    ],
    'JOKER_COLOUR': "joker",
}

TICKET_TO_RIDE_CONFIG = {
    'NR_OF_AGENTS': 3,
    'NR_OF_DESTINATION_CARDS': 2,
    'NR_OF_TRAINS': 45,
    'NR_TRAIN_CARDS': 4,
    'ROUTE_CARDS_PATH': "data/destinations_all.txt",
    'MIN_TRAINS': 2,
    'MAX_TURNS': 50
}

BOARD_CONFIG = {
    'CITY_FILE_PATH': "data/cities.txt",
    'CONNECTION_FILE_PATH': "data/train_routes_all.txt",
    'GRAY_COLOUR': "gray",
    'TRAIN_POINTS': {
        1: 1,
        2: 2,
        3: 4,
        4: 7,
        6: 15,
        8: 21
    }
}

PY_GAME_CONFIG = {
    'SCREEN_WIDTH': 1550,
    'SCREEN_HEIGHT': 900,
    'CONTENT_WIDTH': 1200,
    'PANEL_WIDTH': 350,
    'WIDTH_BUFFER': 2,
    'HEIGHT_BUFFER': 2,
    'BUFFER_FACTOR': 20,
    'LINE_THICKNESS': 4,
    'LINE_THICKNESS_RELATION': 2,
    'RADIUS': 12,
    'BUTTON_WIDTH': 200,
    'BUTTON_HEIGHT': 30

}

PY_GAME_COLOUR_CONFIG = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 234, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'pink': (255, 182, 193),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (180, 180, 180),
    'dark gray': (90, 90, 90),
    'background': (254, 235, 201),
    'background2': (191, 213, 232)
}

AGENT_COLOURS = {
    'dark blue': (3, 0, 114),
    'red': (200, 0, 3),
    'yellow': (215, 185, 42),
    'dark pink': (163, 18, 134),
    'light green': (39, 185, 185)
}