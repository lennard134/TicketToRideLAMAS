"""
Main file for the PyGame window responsible for both displaying the game board and the state space
"""

# TODO: take care of ferries
#       consider ownership
#       check double connections
#       Relations in state space

# Modules
import math
import pygame
import numpy as np

# Model imports
from src.model.TicketToRide import TicketToRide
from src.model.map.City import City
from src.model import config

# Config in PY_GAME_CONFIG file

SCREEN_WIDTH = config.PY_GAME_CONFIG['SCREEN_WIDTH']
SCREEN_HEIGHT = config.PY_GAME_CONFIG['SCREEN_HEIGHT']
CONTENT_WIDTH = config.PY_GAME_CONFIG['CONTENT_WIDTH']
PANEL_WIDTH = config.PY_GAME_CONFIG['PANEL_WIDTH']
WIDTH_BUFFER = config.PY_GAME_CONFIG['WIDTH_BUFFER']
HEIGHT_BUFFER = config.PY_GAME_CONFIG['HEIGHT_BUFFER']
BUFFER_FACTOR = config.PY_GAME_CONFIG['BUFFER_FACTOR']
LINE_THICKNESS = config.PY_GAME_CONFIG['LINE_THICKNESS']
LINE_THICKNESS_RELATION = config.PY_GAME_CONFIG['LINE_THICKNESS_RELATION']
RADIUS = config.PY_GAME_CONFIG['RADIUS']
COLOURS = config.PY_GAME_COLOUR_CONFIG

# Button settings
BUTTON_WIDTH = config.PY_GAME_CONFIG['BUTTON_WIDTH']
BUTTON_HEIGHT = config.PY_GAME_CONFIG['BUTTON_HEIGHT']
BUTTON_COLOUR_LIGHT = (180, 180, 180)
BUTTON_COLOUR_DARK = (110, 110, 110)


class GameBoard(object):
    # def __init__(self, game: Game):
    #     self.game = game

    def __init__(self, ttr: TicketToRide):
        self.ttr = ttr
        self.agent_colors = {}

        self._init_agent_colours()

    def _init_agent_colours(self):
        for agent in self.ttr.agents:
            self.agent_colors[agent.agent_id] = color = list(np.random.choice(range(256), size=3))

    def highest_xy(self, cities: list[City]) -> (int, int):
        """
        Determines maximum x and y coordinates of cities to allow for accurate scaling to window size
        """
        max_y, max_x = cities[0].coordinates

        for city in cities:
            height, width = city.coordinates
            max_x = width if width > max_x else max_x
            max_y = height if height > max_y else max_y

        return max_x, max_y

    def lowest_xy(self, cities: list[City]) -> (int, int):
        """
        Determines minimum x and y coordinates of cities to allow for accurate translation to fit window size
        """
        min_y, min_x = cities[0].coordinates

        for city in cities:
            height, width = city.coordinates
            min_x = width if width < min_x else min_x
            min_y = height if height < min_y else min_y

        return min_x, min_y

    def update_limits(self, x: int, y: int, left: int, right: int, top: int, bottom: int) -> (int, int, int, int):
        """
        Updates the furthest coordinates on all sides to allow for accurate scaling
        """
        left = x if not left or x < left else left
        right = x if not right or x > right else right
        top = y if not top or y < top else top
        bottom = y if not bottom or y > bottom else bottom

        return left, right, top, bottom

    def draw_dashed_line(self, surface: pygame.Surface, color: tuple, start_pos: tuple, end_pos: tuple,
                         width=LINE_THICKNESS, dash_length=10, exclude_corners=True) -> list[pygame.Rect]:
        """
        Draws a dashed line between the given starting and ending position
        """
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

    def compute_circular_coordinates(self, num: int) -> list[tuple[float, float]]:
        """
        Returns a list of num points on a circle
        """
        if num == 0:
            num = 1000
        r = (min(CONTENT_WIDTH, SCREEN_HEIGHT) - WIDTH_BUFFER * BUFFER_FACTOR) / 2
        points = [(int(math.cos(2 * math.pi / num * x) * r + CONTENT_WIDTH / 2),
                   int(math.sin(2 * math.pi / num * x) * r + SCREEN_HEIGHT / 2)) for x in range(0, num + 1)]
        return points

    def rectangle_collision(self, x_left, y_top, x_right, y_bottom, mouse):
        """
        Returns True if the mouse is above the button, else False
        """
        return SCREEN_WIDTH - PANEL_WIDTH + x_left <= mouse[0] \
               <= SCREEN_WIDTH - PANEL_WIDTH + x_right and y_top <= mouse[1] \
               <= y_bottom

    def draw_ttr_board(self, contents: pygame.Surface) -> pygame.Surface:
        """
        Returns the contents of the Ticket to Ride board
        """
        lt_lim = None
        rt_lim = None
        tp_lim = None
        bt_lim = None

        contents.fill(COLOURS['background'])

        min_x, min_y = self.lowest_xy(list(self.ttr.board.cities.values()))
        max_x, max_y = self.highest_xy(list(self.ttr.board.cities.values()))

        min_x -= WIDTH_BUFFER
        max_x += WIDTH_BUFFER
        min_y -= HEIGHT_BUFFER
        max_y += HEIGHT_BUFFER

        max_x -= min_x
        max_y -= min_y

        x_scaling = CONTENT_WIDTH / max_x
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
                pygame.draw.line(contents, color=COLOURS[connection.color], start_pos=(n1x, n1y), end_pos=(n2x, n2y),
                                 width=LINE_THICKNESS)
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
            font1 = pygame.font.SysFont('chalkduster.ttf', 24)
            text = font1.render(city.name, True, (0, 0, 0))

            txt_left = width * x_scaling - 0.5 * text.get_width()
            txt_top = SCREEN_HEIGHT - (height * y_scaling + 0.5 * text.get_height())
            txt_right = width * x_scaling + 0.5 * text.get_width()
            txt_bottom = SCREEN_HEIGHT - (height * y_scaling - 0.5 * text.get_height())

            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(txt_left, txt_top, lt_lim, rt_lim, tp_lim, bt_lim)
            lt_lim, rt_lim, tp_lim, bt_lim = self.update_limits(txt_right, txt_bottom, lt_lim, rt_lim, tp_lim, bt_lim)

            contents.blit(text, (txt_left, txt_top))

        return contents

    def draw_state_space(self, contents: pygame.Surface) -> pygame.Surface:
        """
        Returns the contents of the visual representation of the state space
        """
        contents.fill(COLOURS['background'])

        model = self.ttr.kripke
        coordinates = self.compute_circular_coordinates(len(model.worlds))

        world_coordinate_tuples = {}

        for world, coordinate_tuple in zip(model.worlds, coordinates):
            world_coordinate_tuples[world] = coordinate_tuple

        # draw relations with color per agent {'agent_id': [(world, world), ...], ...}
        for agent_id in model.relations.keys():
            agent_colour = self.agent_colors[agent_id]
            relations_list = model.relations[agent_id]

            for relation_tuple in relations_list:
                world1, world2 = relation_tuple

                start_pos = world_coordinate_tuples[world1]
                end_pos = world_coordinate_tuples[world2]

                pygame.draw.line(contents, color=agent_colour, start_pos=start_pos, end_pos=end_pos,
                                 width=LINE_THICKNESS_RELATION)

        # draw worlds
        for _, coordinate_tuple in world_coordinate_tuples.items():
            pygame.draw.circle(contents, (255, 0, 0), coordinate_tuple, radius=RADIUS)

        return contents

    def draw_side_panel(self, side_panel: pygame.Surface, mouse):
        pass

    def draw_button(self, surface, button_x_left, button_y_top, button_x_right, button_y_bottom, mouse, font, content):
        """
        Function responsible for drawing a single button in the provided surface (side panel)
        """
        if self.rectangle_collision(button_x_left, button_y_top, button_x_right, button_y_bottom, mouse):
            pygame.draw.rect(surface, BUTTON_COLOUR_DARK,
                             [button_x_left, button_y_top, BUTTON_WIDTH, BUTTON_HEIGHT])
        else:
            pygame.draw.rect(surface, BUTTON_COLOUR_LIGHT,
                             [button_x_left, button_y_top, BUTTON_WIDTH, BUTTON_HEIGHT])

        text = font.render(content, True, (0, 0, 0))
        txt_left = button_x_left + BUTTON_WIDTH / 2 - 0.5 * text.get_width()
        txt_top = button_y_top + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
        surface.blit(text, (txt_left, txt_top))

        return surface

    def run(self):
        """
        Main PyGame function responsible for keeping the screen up to date
        """
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        contents = screen.copy()
        contents = pygame.transform.scale(contents, (CONTENT_WIDTH, SCREEN_HEIGHT))

        side_panel = pygame.Surface((SCREEN_WIDTH - CONTENT_WIDTH, SCREEN_HEIGHT))
        side_panel.fill(COLOURS['background2'])

        contents = self.draw_ttr_board(contents)

        screen.blit(contents, (WIDTH_BUFFER / 2, HEIGHT_BUFFER / 2))

        pygame.display.update()

        running = True
        show_board = True

        while running:
            button_x_left = PANEL_WIDTH / 2 - BUTTON_WIDTH / 2
            button_x_right = PANEL_WIDTH / 2 + BUTTON_WIDTH / 2

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rectangle_collision(button_x_left, BUTTON_HEIGHT / 2,
                                                button_x_right, BUTTON_HEIGHT / 2 + BUTTON_HEIGHT, mouse):
                        show_board = False if show_board else True

            if show_board:
                contents = self.draw_ttr_board(contents)
            else:
                contents = self.draw_state_space(contents)

            button_font = pygame.font.SysFont('chalkduster.ttf', 20)

            # draw switch button
            side_panel = self.draw_button(side_panel, button_x_left, BUTTON_HEIGHT / 2,
                                          button_x_right, BUTTON_HEIGHT / 2 + BUTTON_HEIGHT,
                                          mouse, button_font, "Switch View")

            # draw turn button
            side_panel = self.draw_button(side_panel, button_x_left, BUTTON_HEIGHT / 2 + 2 * BUTTON_HEIGHT,
                                          button_x_right, BUTTON_HEIGHT / 2 + 3 * BUTTON_HEIGHT,
                                          mouse, button_font, "Turn")

            screen.blit(contents, (WIDTH_BUFFER / 2, HEIGHT_BUFFER / 2 - 1))
            screen.blit(side_panel, (CONTENT_WIDTH, 0))
            pygame.display.update()


if __name__ == "__main__":
    ttr = TicketToRide()
    game_board = GameBoard(ttr)
    game_board.run()
