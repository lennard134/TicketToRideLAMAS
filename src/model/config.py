"""
Config file containing settings for different classes in the form of a dictionary
"""

AGENT_CONFIG = {
    'START_SCORE': 0,
    'NR_CARDS_TO_DRAW': 2
}

DECK_CONFIG = {
    'NR_COLOUR_CARDS': 12,
    'NR_TRAINS': 14,
    'NR_OPEN_CARDS': 5,
    'TRAIN_COLOURS': [
        'red', 'pink', 'white', 'yellow', 'green', 'blue', 'black', 'orange'
    ],
    'JOKER_COLOUR': "joker",
}

TICKET_TO_RIDE_CONFIG = {
    'NR_OF_AGENTS': 3,
    'NR_OF_TRAINS': 20,
    'NR_OF_DESTINATION_CARDS': 2,
    'NR_TRAIN_CARDS': 4,
    'ROUTE_CARDS_PATH': "data/destinations_all.txt",
    'MIN_TRAINS': 2
}

BOARD_CONFIG = {
    'CITY_FILE_PATH': "data/cities.txt",
    'CONNECTION_FILE_PATH': "data/train_routes_all.txt"
}

PY_GAME_CONFIG = {
    'SCREEN_WIDTH': 1400,
    'SCREEN_HEIGHT': 900,
    'CONTENT_WIDTH': 1200,
    'PANEL_WIDTH': 200,
    'WIDTH_BUFFER': 2,
    'HEIGHT_BUFFER': 2,
    'BUFFER_FACTOR': 20,
    'LINE_THICKNESS': 4,
    'LINE_THICKNESS_RELATION' : 1,
    'RADIUS': 12,
    'BUTTON_WIDTH': 100,
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
    'background': (254, 235, 201),
    'background2': (191, 213, 232)
}