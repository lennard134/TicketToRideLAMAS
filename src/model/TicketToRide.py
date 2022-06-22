"""
Object Ticket to ride board game that has all the functionalities of the game
"""

# packages
import random

from src.model.Deck import Deck
from src.model.map.Board import Board
from src.model.Agent import Agent
from src.model.RouteCard import RouteCard
from src.model.Game import Game
from src.model.TtRKripke.TtRKripke import TtRKripke

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# settings
NR_OF_AGENTS = 3
NR_OF_TRAINS = 10
ROUTE_CARDS_PATH = os.path.join(ROOT_DIR, "data/destinations_all.txt")


class TicketToRide(object):

    def __init__(self):
        """
        Initialize the full game by initializing agent, board, deck and route cards individually
        """
        self.deck = Deck()
        self.board = Board()
        self.agents = []
        self.route_cards = []
        self.kripke = None

        self._init_agents()
        self._init_route_cards()

        self._init_kripke()

    def _init_agents(self):
        """
        Initialize all agents
        """
        for idx in range(NR_OF_AGENTS):
            self.agents.append(Agent(idx, NR_OF_TRAINS))

    def _init_route_cards(self):
        """
        Read route cards from text file and create new RouteCard objects for every card which are stored in an array
        """
        with open(ROUTE_CARDS_PATH, mode='r', encoding='utf-8') as f:
            for line in f:
                line_list = line.split()
                start = self.board.get_city(line_list[0].split('-')[0])
                end = self.board.get_city(line_list[0].split('-')[1])

                if start is None or end is None:
                    print(f'Cities {start} or {end} not implemented. Skipping....')
                    continue

                score = int(line_list[1].rpartition('(')[2].partition(')')[0])
                self.route_cards.append(RouteCard(start, end, score))

        random.shuffle(self.route_cards)
        print(len(self.route_cards))

        for route_card in self.route_cards:
            print(route_card)

        left_over_cards = len(self.route_cards) % NR_OF_AGENTS

        if left_over_cards > 0:
            print(f"Deleting {left_over_cards} route cards.")
            del self.route_cards[-left_over_cards:]

    def _init_kripke(self):
        agent_ids = []
        route_card_ids = []
        for agent in self.agents:
            agent_ids.append(agent.agent_id)
        for route_card in route_card_ids:
            route_card_ids.append(route_card.route_name)

        self.kripke = TtRKripke(agent_ids=agent_ids, route_cards_ids=route_card_ids)

    def _distribute_route_cards(self):
        """
        Distribute route cards among the agents
        """
        random.shuffle(self.route_cards)
        step_size = len(self.route_cards) // len(self.agents)
        end = 0
        for agent in self.agents:
            begin = end
            end = begin + step_size
            for card in self.route_cards[begin:end]:
                agent.add_route_card(card)
                self.kripke.update_relations(agent.agent_id, agent.agent_id, card.route_name)

    def _distribute_train_cards(self):
        """
        Give each agent four coloured cards from the deck
        """
        for agent in self.agents:
            for _ in range(4):
                agent.add_train_card(self.deck.remove_closed_card())

    def _make_route_card_dict(self) -> dict:
        """
        Make route cards dictionary
        """
        route_card_dict = {}
        for route_card in self.route_cards:
            route_card_dict[route_card.route_name] = route_card
        return route_card_dict

    def play(self):
        """
        Game loop for the Ticket to Ride game
        """
        self._distribute_route_cards()
        self._distribute_train_cards()

        # Init game model
        route_card_dict = self._make_route_card_dict()
        game = Game(board=self.board, route_cards=route_card_dict, agent_list=self.agents, deck=self.deck,
                    model=self.kripke)
        for agent in self.agents:
            agent.set_game(game)
        game.init_shortest_routes()

        # announce cards in game and compute all optimal routes
        in_game = True

        while in_game:
            for agent in self.agents:
                agent.choose_action()
            in_game = False

        print("!!GAME OVER!!")


if __name__ == "__main__":
    ttr = TicketToRide()
    ttr.play()

