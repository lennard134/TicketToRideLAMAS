"""
Main file for the PyGame window responsible for both displaying the game board and the state space
"""

# Modules
import pygame

# Model imports
from src.model.TicketToRide import TicketToRide
from src.model.map.City import City

# Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000


class GameBoard(object):
    # def __init__(self, game: Game):
    #     self.game = game

    def __init__(self, ttr: TicketToRide):
        self.ttr = ttr

    def highest_xy(self, cities: list[City], min_x: float, min_y: float):
        """
        Determines maximum x and y coordinates of cities to allow for accurate scaling to window size
        """
        max_y, max_x = cities[0].coordinates
        max_x -= min_x
        max_y -= min_y

        for city in cities:
            height, width = city.coordinates
            height -= min_y
            width -= min_x
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

    def run(self):
        """
        Main PyGame function responsible for keeping the screen up to date
        """
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        contents = screen.copy()
        clock = pygame.time.Clock()

        screen.fill((255, 255, 255))
        contents.fill((255, 255, 255))

        # screen.fill((0, 0, 0,))

        font1 = pygame.font.SysFont('chalkduster.ttf', 24)

        min_x, min_y = self.lowest_xy(list(self.ttr.board.cities.values()))
        max_x, max_y = self.highest_xy(list(self.ttr.board.cities.values()), min_x, min_y)

        x_scaling = SCREEN_WIDTH / max_x
        y_scaling = SCREEN_HEIGHT / max_y

        for connection in self.ttr.board.connections:
            n1h, n1w = connection.start_point.coordinates
            n2h, n2w = connection.end_point.coordinates
            n1x = (n1w - min_x) * x_scaling
            n2x = (n2w - min_x) * x_scaling
            n1y = (n1h - min_y) * y_scaling
            n2y = (n2h - min_y) * y_scaling
            # draw edges
            pygame.draw.line(contents, (100, 100, 100), (n1x, SCREEN_HEIGHT - n1y), (n2x, SCREEN_HEIGHT - n2y), 2)

        for city in self.ttr.board.cities.values():
            height, width = city.coordinates
            height -= min_y
            width -= min_x
            # draw cities as circles

            pygame.draw.circle(contents, (255, 0, 0), (width * x_scaling, SCREEN_HEIGHT - height * y_scaling),
                               radius=12)
            # draw text on center of cities
            text = font1.render(city.name, True, (0, 0, 0))
            txt_left = width * x_scaling - 0.5 * text.get_width()
            txt_top = SCREEN_HEIGHT - (height * y_scaling + 0.5 * text.get_height())
            contents.blit(text, (txt_left, txt_top))

        screen.blit(contents, (0, 0))

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
