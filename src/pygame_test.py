import pygame

# from src.model.Game import Game
from src.model.TicketToRide import TicketToRide

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameBoard(object):
    def __init__(self, ttr: TicketToRide, game: Game):
        # self.game = game
        self.ttr = ttr

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        screen.fill((255, 255, 255))

        # n1 = (70, 210)
        # n2 = (200, 500)
        # n3 = (600, 100)
        # nodes = [n1, n2, n3]
        # edges = [(n1, n2), (n2, n3)]

        screen.fill((0, 0, 0,))

        for connection in self.ttr.route_cards:  # draw edges
            n1 = connection.start_point.coordinates
            n2 = connection.end_point.coordinates
            pygame.draw.line(screen, (100, 100, 100), n1, n2, 2)

        for city in self.ttr.board.cities:  # draw nodes
            pygame.draw.circle(screen, (255, 0, 0), city.coordinates, radius=12)

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
