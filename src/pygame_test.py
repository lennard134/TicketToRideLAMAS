"""
Main file for the PyGame window responsible for both displaying the game board and the state space
"""

# TODO: take care of ferries

# Modules
import pygame
import numpy as np

# Model imports
from src.model.TicketToRide import TicketToRide
from src.model.map.City import City

# Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
WIDTH_BUFFER = 2
HEIGHT_BUFFER = 2
LINE_THICKNESS = 4
RADIUS = 12
COLOURS = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 234, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'pink': (255, 182, 193),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (180, 180, 180),
    'background': (254, 235, 201)
}


class GameBoard(object):
    # def __init__(self, game: Game):
    #     self.game = game

    def __init__(self, ttr: TicketToRide):
        self.ttr = ttr

    def highest_xy(self, cities: list[City]):
        """
        Determines maximum x and y coordinates of cities to allow for accurate scaling to window size
        """
        max_y, max_x = cities[0].coordinates

        for city in cities:
            height, width = city.coordinates
            max_x = width if width > max_x else max_x
            max_y = height if height > max_y else max_y

        return max_x, max_y

    def lowest_xy(self, cities: list[City]):
        """
        Determines minimum x and y coordinates of cities to allow for accurate translation to fit window size
        """
        min_y, min_x = cities[0].coordinates

        for city in cities:
            height, width = city.coordinates
            min_x = width if width < min_x else min_x
            min_y = height if height < min_y else min_y

        return min_x, min_y

    def update_limits(self, x, y, left, right, top, bottom):
        """
        Updates the furthest coordinates on all sides to allow for accurate scaling
        """
        left = x if not left or x < left else left
        right = x if not right or x > right else right
        top = y if not top or y < top else top
        bottom = y if not bottom or y > bottom else bottom

        return left, right, top, bottom

    def draw_dashed_line(self, surface, color, start_pos, end_pos, width=LINE_THICKNESS, dash_length=10, exclude_corners=True):
        # convert tuples to numpy arrays
        start_pos = np.array(start_pos)
        end_pos = np.array(end_pos)

        # get euclidian distance between start_pos and end_pos
        length = np.linalg.norm(end_pos - start_pos)

        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        dash_amount = int(length / dash_length)

        # x-y-value-pairs of where dashes start (and on next, will end)
        dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

        return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n + 1]), width)
                for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

    def run(self):
        """
        Main PyGame function responsible for keeping the screen up to date
        """
        lt_lim = None
        rt_lim = None
        tp_lim = None
        bt_lim = None

        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        contents = screen.copy()
        clock = pygame.time.Clock()

        screen.fill(COLOURS['background'])
        contents.fill(COLOURS['background'])

        font1 = pygame.font.SysFont('chalkduster.ttf', 24)

        min_x, min_y = self.lowest_xy(list(self.ttr.board.cities.values()))
        max_x, max_y = self.highest_xy(list(self.ttr.board.cities.values()))

        min_x -= WIDTH_BUFFER
        max_x += WIDTH_BUFFER
        min_y -= HEIGHT_BUFFER
        max_y += HEIGHT_BUFFER

        max_x -= min_x
        max_y -= min_y

        x_scaling = SCREEN_WIDTH / max_x
        y_scaling = SCREEN_HEIGHT / max_y

        for connection in self.ttr.board.connections:
            n1h, n1w = connection.start_point.coordinates
            n2h, n2w = connection.end_point.coordinates
            n1x = (n1w - min_x) * x_scaling
            n2x = (n2w - min_x) * x_scaling
            n1y = SCREEN_HEIGHT - (n1h - min_y) * y_scaling
            n2y = SCREEN_HEIGHT - (n2h - min_y) * y_scaling

            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(n1x, n1y, lt_lim, rt_lim, tp_lim, bt_lim)
            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(n2x, n2y, lt_lim, rt_lim, tp_lim, bt_lim)

            # draw edges
            if connection.color in COLOURS:
                pygame.draw.line(contents, color=COLOURS[connection.color], start_pos=(n1x, n1y), end_pos=(n2x, n2y), width=LINE_THICKNESS)
            else:
                self.draw_dashed_line(contents, COLOURS['gray'], (n1x, n1y), (n2x, n2y))

        for city in self.ttr.board.cities.values():
            height, width = city.coordinates
            height -= min_y
            width -= min_x

            x = width * x_scaling
            y = SCREEN_HEIGHT - height * y_scaling

            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(x - RADIUS, y - RADIUS, lt_lim, rt_lim, tp_lim, bt_lim)
            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(x + RADIUS, y + RADIUS, lt_lim, rt_lim, tp_lim, bt_lim)

            # draw cities as circles
            pygame.draw.circle(contents, (255, 0, 0), (x, y), radius=RADIUS)

            # draw text on center of cities
            text = font1.render(city.name, True, (0, 0, 0))

            txt_left = width * x_scaling - 0.5 * text.get_width()
            txt_top = SCREEN_HEIGHT - (height * y_scaling + 0.5 * text.get_height())
            txt_right = width * x_scaling + 0.5 * text.get_width()
            txt_bottom = SCREEN_HEIGHT - (height * y_scaling - 0.5 * text.get_height())

            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(txt_left, txt_top, lt_lim, rt_lim, tp_lim, bt_lim)
            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(txt_right, txt_bottom, lt_lim, rt_lim, tp_lim, bt_lim)

            contents.blit(text, (txt_left, txt_top))

        screen.blit(contents, (WIDTH_BUFFER / 2, HEIGHT_BUFFER / 2))

        pygame.display.update()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == "__main__":
    ttr = TicketToRide()
    game_board = GameBoard(ttr)
    game_board.run()
