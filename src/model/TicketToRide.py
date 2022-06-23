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
from src.model import config
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Data in TICKET_TO_RIDE_CONFIG
NR_OF_AGENTS = config.TICKET_TO_RIDE_CONFIG['NR_OF_AGENTS']
NR_OF_TRAINS = config.TICKET_TO_RIDE_CONFIG['NR_OF_TRAINS']
NR_TRAIN_CARDS = config.TICKET_TO_RIDE_CONFIG['NR_TRAIN_CARDS']
ROUTE_CARDS_PATH = os.path.join(ROOT_DIR, config.TICKET_TO_RIDE_CONFIG['ROUTE_CARDS_PATH'])
MIN_TRAINS = config.TICKET_TO_RIDE_CONFIG['MIN_TRAINS']


class TicketToRide(object):

    def __init__(self):
        """
        Initialize the full game by initializing agent, board, deck and route cards individually
        """
        self.deck = None
        self.board = None
        self.agents = []
        self.route_cards = []
        self.turn_num = 0
        self.kripke = None
        self.last_turn = None
        self.in_game = True

    def _init_agents(self):
        """
        Initialize all agents
        """
        for idx in range(NR_OF_AGENTS):
            self.agents.append(Agent(idx, NR_OF_TRAINS))

    def _init_route_cards(self, max_nr_route_cards_per_agent=2):
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
        print(f"Number of route cards = {len(self.route_cards)}")

        if len(self.route_cards) // NR_OF_AGENTS > max_nr_route_cards_per_agent:
            print(f"Removing {len(self.route_cards) - max_nr_route_cards_per_agent * NR_OF_AGENTS} route cards")
            del self.route_cards[-(len(self.route_cards) - max_nr_route_cards_per_agent * NR_OF_AGENTS):]

        left_over_cards = len(self.route_cards) % NR_OF_AGENTS
        if left_over_cards > 0:
            print(f"Deleting {left_over_cards} route cards.")
            del self.route_cards[-left_over_cards:]

        for route_card in self.route_cards:
            print(f"- {route_card}")

    def _init_kripke(self):
        agent_ids = []
        route_card_ids = []
        for agent in self.agents:
            agent_ids.append(agent.agent_id)
        for route_card in self.route_cards:
            route_card_ids.append(route_card.route_name)

        print(f"agent_ids = {agent_ids}, route_cards = {route_card_ids}")
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
                self.kripke.update_once_cards_known(agent.agent_id, {card.route_name})

    def _distribute_train_cards(self):
        """
        Give each agent four coloured cards from the deck
        """
        for agent in self.agents:
            for _ in range(NR_TRAIN_CARDS):
                agent.add_train_card(self.deck.remove_closed_card())

    def _make_route_card_dict(self) -> dict:
        """
        Make route cards dictionary
        """
        route_card_dict = {}
        for route_card in self.route_cards:
            route_card_dict[route_card.route_name] = route_card
        return route_card_dict

    def is_finished(self, agent_turn: int) -> bool:
        """
        Function that checks if the game is finished based on
        :return: True if game is finished, else False
        """

        for agent in self.agents:
            # check if an agent has finished all route_cards
            if agent.check_if_route_cards_done():
                print(f"--------------------------------------------------------\n"
                      f"----------- AGENT {agent.agent_id} FINISHED ALL ROUTE CARDS ---------------\n"
                      f"--------------------------------------------------------")
                return True

        # check if an agent has less than 3 trains left, then everyone has only one turn left
        if self.last_turn is None:
            for agent in self.agents:
                if agent.nr_of_trains < MIN_TRAINS:
                    self.last_turn = agent.agent_id
                    print(f"--------------------------------------------------------\n"
                          f"----------- AGENT {agent.agent_id} has less than {MIN_TRAINS} ---------------\n"
                          f"--------------------------------------------------------")
        elif agent_turn == self.last_turn:
            print(f"--------------------------------------------------------\n"
                  f"----------- AGENT {agent_turn} has played its last turn ---------------\n"
                  f"--------------------------------------------------------")
            return True

        # check if all agents could have drawn a card (deck nonempty)
        finished = True
        for agent in self.agents:
            if agent.can_draw_card:
                finished = False
        if finished:
            print(f"--------------------------------------------------------\n"
                  f"----------- All agents could not have drawn cards ---------------\n"
                  f"--------------------------------------------------------")
        return finished

    def init_game(self):
        self.deck = Deck()
        self.board = Board()
        self.agents = []
        self.route_cards = []
        self.turn_num = 0
        self.kripke = None
        self.last_turn = None
        self.in_game = True

        self._init_agents()
        self._init_route_cards()
        self._init_kripke()
        self._distribute_route_cards()
        self._distribute_train_cards()

        # Init game model
        route_card_dict = self._make_route_card_dict()
        game = Game(board=self.board, route_cards=route_card_dict, agent_list=self.agents, deck=self.deck,
                    model=self.kripke)
        for agent in self.agents:
            agent.set_game(game)
        game.init_shortest_routes()

    def turn(self):
        print("\n\n----------------------------------------\n"
              f"--- TURN {self.turn_num}\n"
              "----------------------------------------\n")
        for connection in self.board.connections:
            if connection.owner is not None:
                print(f"--> connection {connection.start_point.name}-{connection.end_point.name} has owner {connection.owner}.")

        for agent in self.agents:
            agent.choose_action()
            if self.is_finished(agent.agent_id):
                self.in_game = False
                return

        self.turn_num += 1

    def play(self):
        """
        Game loop for the Ticket to Ride game
        """
        self.init_game()
        while self.in_game:
            self.turn()
        print(f"Thanks for playing with Jeroen!! He loved it!")


if __name__ == "__main__":
    ttr = TicketToRide()
    ttr.play()

