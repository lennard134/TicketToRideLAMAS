"""
Main file for the PyGame window responsible for both displaying the game board and the state space
"""

# Modules
import math
import pygame
import numpy as np
import random

# Model imports
from src.model.TicketToRide import TicketToRide
from src.model.map.City import City
from src.model import config

# Config in PY_GAME_CONFIG file
from src.model.map.Connection import FerryConnection

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
AGENT_COLOURS = config.AGENT_COLOURS

# Button settings
BUTTON_WIDTH = config.PY_GAME_CONFIG['BUTTON_WIDTH']
BUTTON_HEIGHT = config.PY_GAME_CONFIG['BUTTON_HEIGHT']
BUTTON_COLOUR_LIGHT = (180, 180, 180)
BUTTON_COLOUR_DARK = (110, 110, 110)


class Visualizer(object):
    # def __init__(self, game: Game):
    #     self.game = game

    def __init__(self, ttr: TicketToRide):
        self.ttr = ttr
        self.agent_colors = {}
        self.state_coordinates = {}
        self.selected_state_coordinates_tuple = None

        self._init_agent_colours()

    def _init_agent_colours(self):
        """
        Randomly assign agents a color from the AGENT_COLOURS dictionary
        """
        colours = random.sample(list(AGENT_COLOURS.values()), len(self.ttr.agents))
        for agent, colour in zip(self.ttr.agents, colours):
            # self.agent_colors[agent.agent_id] = color = list(np.random.choice(range(256), size=3))
            self.agent_colors[agent.agent_id] = colour

    def highest_xy(self, cities: list[City]) -> (int, int):
        """
        Determines maximum x and y coordinates of cities to allow for accurate scaling to window size
        :param cities: list of cities for which the highest x and y coordinates need to be determined
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
        :param cities: list of cities for which the lowest x and y coordinates need to be determined
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
        :param x: x coordinate
        :param y: y coordinate
        :param left: furthest left coordinate
        :param right: furthest right coordinate
        :param top: furthest top coordinate
        :param bottom: furthest bottom coordinate
        :return: updated left, right, top and bottom coordinates
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
        :param surface: PyGame surface on which drawing of dashed line is done
        :param color: color of the line
        :param start_pos: start coordinate tuple
        :param end_pos: end coordinate tuple
        :param width: line width
        :param dash_length: length of individual dashes
        :param exclude_corners: boolean to exclude
        :return: individually drawn line sections on the surface
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
        :param num: number of points on the circle
        :return: list of coordinate tuples of length num
        """
        if num == 0:
            num = 1000
        r = (min(CONTENT_WIDTH, SCREEN_HEIGHT) - WIDTH_BUFFER * BUFFER_FACTOR) / 2
        points = [(int(math.cos(2 * math.pi / num * x) * r + CONTENT_WIDTH / 2),
                   int(math.sin(2 * math.pi / num * x) * r + SCREEN_HEIGHT / 2)) for x in range(0, num)]
        return points

    def rectangle_collision(self, x_left: int, y_top: int, x_right: int, y_bottom: int, mouse: tuple[int, int]) -> bool:
        """
        Returns True if the mouse is above the button, else False
        :param x_left: left x coordinate of rectangle
        :param y_top: top y coordinate of rectangle
        :param x_right: right x coordinate of rectangle
        :param y_bottom: bottom y coordinate of rectangle
        :param mouse: tuple containing current mouse location
        :return: boolean indicating whether or not the mouse is situated within boundaries of rectangle
        """
        return SCREEN_WIDTH - PANEL_WIDTH + x_left <= mouse[0] \
               <= SCREEN_WIDTH - PANEL_WIDTH + x_right and y_top <= mouse[1] \
               <= y_bottom

    def state_collision(self, mouse):
        """
        Returns True if mouse has collision with a circle from the set of state coordinates
        :param mouse: tuple with mouse coordinates
        :return: boolean indicating truth of collision
        """
        for world, coordinates in self.state_coordinates.items():
            centerx, centery = coordinates
            dist_x = mouse[0] - centerx
            dist_y = mouse[1] - centery
            # Calculate the length of the hypotenuse. If it's less than the
            # radius, the mouse collides with the circle.
            if math.hypot(dist_x, dist_y) < RADIUS:
                if self.selected_state_coordinates_tuple and self.selected_state_coordinates_tuple == (world, centerx, centery):
                    self.selected_state_coordinates_tuple = None
                    return False
                self.selected_state_coordinates_tuple = (world, centerx, centery)
                print('collision')
                return True
        self.selected_state_coordinates_tuple = None
        return False

    def show_state_info(self, surface, text_left, text_height, font):
        """
        Adds information of selected world to the side panel
        :param surface: PyGame surface object on which the text ought to be drawn
        :param text_left: left coordinate of all text
        :param text_height: height of text
        :param font: font used in all other text of side panel
        :return: updated surface with added state info
        """
        world, _, _ = self.selected_state_coordinates_tuple

        text_height += BUTTON_HEIGHT
        text = font.render(f"Selected world:", True, COLOURS['dark gray'])
        txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
        surface.blit(text, (text_left, txt_top))

        # print(f'world {world.get_name()} has agent_list {world._agent_list}')
        for agent_id in self.agent_colors.keys():
            if world.has_agent_in_agent_list(agent_id, agent_id):
                color = self.agent_colors[agent_id]
            else:
                color = COLOURS['dark gray']

            text_height += BUTTON_HEIGHT / 2
            text = font.render(f"Agent {agent_id}:", True, color)
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            surface.blit(text, (text_left, txt_top))

            for route_name in world.get_state(agent_id):
                text_height += BUTTON_HEIGHT / 2
                text = font.render(f"* {route_name}", True, color)
                txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
                surface.blit(text, (text_left, txt_top))

        return surface

    def draw_button(self, surface: pygame.Surface, button_x_left: int, button_y_top: int, button_x_right: int,
                    button_y_bottom: int, mouse: tuple[int, int],
                    font: pygame.font.Font, content: str) -> pygame.Surface:
        """
        Function responsible for drawing a single button in the provided surface (side panel)
        :param surface: PyGame surface on which the button must be drawn
        :param button_x_left: left x coordinate of the button
        :param button_y_top: top y coordinate of the button
        :param button_x_right: right x coordinate of the button
        :param button_y_bottom: bottom y coordinate of the button
        :param mouse: tuple containing the mouse coordinates
        :param font: font to be used for the text in the button
        :param content: string containing the text to be drawn on the button
        :return: PyGame surface containing the newly drawn button
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

    def draw_ttr_board(self, contents: pygame.Surface) -> pygame.Surface:
        """
        Returns the contents of the Ticket to Ride board
        :param contents: PyGame surface on which the ttr board must be drawn
        :return: PyGame surface containing full board contents
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
            if connection.owner is not None:
                color = self.agent_colors[connection.owner]
                line_width = 2*LINE_THICKNESS
            else:
                color = COLOURS[connection.color]
                line_width = LINE_THICKNESS

            if isinstance(connection, FerryConnection):
                self.draw_dashed_line(contents, color, (n1x, n1y), (n2x, n2y), width=line_width)
            else:
                pygame.draw.line(contents, color=color, start_pos=(n1x, n1y), end_pos=(n2x, n2y), width=line_width)

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
        :param contents: PyGame surface on which the state space ought to be drawn
        :return: PyGame surface containing full state spacce
        """
        contents.fill(COLOURS['background'])

        model = self.ttr.kripke
        coordinates = self.compute_circular_coordinates(len(model.worlds))
        random.Random(69).shuffle(coordinates)

        self.state_coordinates = {}

        if len(model.worlds) == 1:
            self.state_coordinates[model.worlds[0]] = (CONTENT_WIDTH / 2, SCREEN_HEIGHT / 2)
        else:
            for world, coordinate_tuple in zip(model.worlds, coordinates):
                self.state_coordinates[world] = coordinate_tuple

        # draw relations with color per agent {'agent_id': [(world, world), ...], ...}
        for agent_id in model.relations.keys():
            agent_colour = self.agent_colors[agent_id]
            relations_list = model.relations[agent_id]

            for relation_tuple in relations_list:
                world1, world2 = relation_tuple

                start_pos = self.state_coordinates[world1]
                end_pos = self.state_coordinates[world2]

                pygame.draw.line(contents, color=agent_colour, start_pos=start_pos, end_pos=end_pos,
                                 width=LINE_THICKNESS_RELATION)

        # draw worlds
        true_state = self.ttr.get_true_state()
        found_true_state = False
        for world, coordinate_tuple in self.state_coordinates.items():
            x, y = coordinate_tuple
            tuple_to_check = (world, x, y)
            if tuple_to_check == self.selected_state_coordinates_tuple:
                pygame.draw.circle(contents, (0, 0, 255), coordinate_tuple, radius=RADIUS)
            else:
                if not found_true_state:
                    for agent in self.ttr.agents:
                        if not true_state[agent.agent_id].symmetric_difference(world.get_state(agent.agent_id)):
                            # true if no difference in states
                            found_true_state = True
                        else:
                            found_true_state = False
                            break
                    if found_true_state:
                        pygame.draw.circle(contents, (0, 255, 0), coordinate_tuple, radius=RADIUS)
                        continue
                pygame.draw.circle(contents, (255, 0, 0), coordinate_tuple, radius=RADIUS)

        return contents

    def draw_side_panel(self, side_panel: pygame.Surface, button_x_left: int, button_x_right: int,
                        mouse: tuple[int, int]) -> pygame.Surface:
        """
        Returns the contents of the side panel
        :param side_panel: PyGame surface on which the side panel ought to be drawn
        :param button_x_left: left coordinate of all buttons in the side panel
        :param button_x_right: right coordinate of all buttons in the side panel
        :param mouse: tuple containing mouse coordinates
        :return: PyGame surface with fully drawn side panel
        """

        side_panel.fill(COLOURS['background2'])
        button_font = pygame.font.SysFont('chalkduster.ttf', 20)

        # draw switch button
        side_panel = self.draw_button(side_panel, button_x_left, BUTTON_HEIGHT / 2,
                                      button_x_right, BUTTON_HEIGHT / 2 + BUTTON_HEIGHT,
                                      mouse, button_font, "Switch View")

        # draw turn button
        side_panel = self.draw_button(side_panel, button_x_left, BUTTON_HEIGHT / 2 + 2 * BUTTON_HEIGHT,
                                      button_x_right, BUTTON_HEIGHT / 2 + 3 * BUTTON_HEIGHT,
                                      mouse, button_font, "Turn")

        # reset game
        side_panel = self.draw_button(side_panel, button_x_left, BUTTON_HEIGHT / 2 + 4 * BUTTON_HEIGHT,
                                      button_x_right, BUTTON_HEIGHT / 2 + 5 * BUTTON_HEIGHT,
                                      mouse, button_font, "Reset")

        # show relevant information of agents
        text_height = 6 * BUTTON_HEIGHT
        txt_left = BUFFER_FACTOR * 2
        for idx, agent in enumerate(self.ttr.agents):
            text = button_font.render(f"Agent {agent.agent_id}", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT / 2
            text = button_font.render(f"* score: {agent.score}", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT / 2
            text = button_font.render(f"* nr. trains: {agent.nr_of_trains}", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT / 2
            text = button_font.render(f"* route cards:", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            for route_card in agent.own_route_cards:
                text_color = COLOURS['dark gray']
                if route_card.is_finished:
                    text_color = self.agent_colors[agent.agent_id]
                text_height += BUTTON_HEIGHT / 2
                text = button_font.render(f"   - {route_card.route_name}", True, text_color)
                txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
                side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT / 2
            text = button_font.render(f"* last move:", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT / 2
            text = button_font.render(f"   - {agent.last_move}", True,
                                      self.agent_colors[agent.agent_id])
            txt_top = BUTTON_HEIGHT / 2 + text_height + BUTTON_HEIGHT / 2 - 0.5 * text.get_height()
            side_panel.blit(text, (txt_left, txt_top))

            text_height += BUTTON_HEIGHT

        # show information of selected state
        if self.selected_state_coordinates_tuple:
            side_panel = self.show_state_info(side_panel, txt_left, text_height, button_font)

        return side_panel

    def run(self):
        """
        Main PyGame function responsible for keeping the screen up to date
        """
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        contents = screen.copy()
        contents = pygame.transform.scale(contents, (CONTENT_WIDTH, SCREEN_HEIGHT))
        side_panel = pygame.Surface((SCREEN_WIDTH - CONTENT_WIDTH, SCREEN_HEIGHT))

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
                    # assert not clicked on state
                    if not self.state_collision(mouse):
                        self.selected_state_coordinates_tuple = None

                    # switch button
                    if self.rectangle_collision(button_x_left, BUTTON_HEIGHT / 2,
                                                button_x_right, BUTTON_HEIGHT / 2 + BUTTON_HEIGHT, mouse):
                        show_board = False if show_board else True

                    # turn button
                    elif self.rectangle_collision(button_x_left, BUTTON_HEIGHT / 2 + 2 * BUTTON_HEIGHT,
                                                  button_x_right, BUTTON_HEIGHT / 2 + 3 * BUTTON_HEIGHT, mouse):
                        self.ttr.turn()

                    # reset button
                    elif self.rectangle_collision(button_x_left, BUTTON_HEIGHT / 2 + 4 * BUTTON_HEIGHT,
                                                  button_x_right, BUTTON_HEIGHT / 2 + 5 * BUTTON_HEIGHT,
                                                  mouse):
                        self.ttr.init_game()

            if show_board:
                contents = self.draw_ttr_board(contents)
            else:
                contents = self.draw_state_space(contents)

            side_panel = self.draw_side_panel(side_panel, button_x_left, button_x_right, mouse)

            screen.blit(contents, (WIDTH_BUFFER / 2, HEIGHT_BUFFER / 2 - 1))
            screen.blit(side_panel, (CONTENT_WIDTH, 0))

            pygame.display.update()


if __name__ == "__main__":
    ttr = TicketToRide()
    visualizer = Visualizer(ttr)
    visualizer.run()
