"""
Object Ticket to ride board game that has all the functionalities of the game
"""

# packages
import random
from .Deck import Deck
from .map.Board import Board
from .Agent import Agent
from .RouteCard import RouteCard
from .Game import Game
from .ttr_kripke.TtRKripke import TtRKripke
from .config import *
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Data in TICKET_TO_RIDE_CONFIG
NR_OF_TRAINS = TICKET_TO_RIDE_CONFIG['NR_OF_TRAINS']
NR_TRAIN_CARDS = TICKET_TO_RIDE_CONFIG['NR_TRAIN_CARDS']
ROUTE_CARDS_PATH = os.path.join(ROOT_DIR, TICKET_TO_RIDE_CONFIG['ROUTE_CARDS_PATH'])
MIN_TRAINS = TICKET_TO_RIDE_CONFIG['MIN_TRAINS']
MAX_TURNS = TICKET_TO_RIDE_CONFIG['MAX_TURNS']


class TicketToRide(object):

    def __init__(self, num_agents: int, num_route_cards: int):
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

        self.init_game(num_agents, num_route_cards)

    def _init_agents(self, num_agents):
        """
        Initialize all agents
        """
        for idx in range(num_agents):
            self.agents.append(Agent(idx, NR_OF_TRAINS))

    def _init_route_cards(self, total_num_route_cards: int):
        """
        Read route cards from text file and create new RouteCard objects for every card which are stored in an array
        """
        with open(ROUTE_CARDS_PATH, mode='r', encoding='utf-8') as f:
            for line in f:
                line_list = line.split()
                start = self.board.get_city(line_list[0].split('-')[0])
                end = self.board.get_city(line_list[0].split('-')[1])

                if start is None or end is None:
                    # print(f'Route_card: Cities {start} or {end} not implemented. Skipping....')
                    continue

                score = int(line_list[1].rpartition('(')[2].partition(')')[0])
                self.route_cards.append(RouteCard(start, end, score))

        random.shuffle(self.route_cards)
        print(f"Number of route cards available = {len(self.route_cards)}")

        if len(self.route_cards) > total_num_route_cards:
            print(f"Removing {len(self.route_cards) - total_num_route_cards} route cards to get a total of "
                  f"{total_num_route_cards} route cards.")
            del self.route_cards[-(len(self.route_cards) - total_num_route_cards):]

        left_over_cards = len(self.route_cards) % len(self.agents)
        if left_over_cards > 0:
            print(f"Deleting {left_over_cards} route cards to evenly distribute cards.")
            del self.route_cards[-left_over_cards:]

        print(f"\nPossible route cards (total={len(self.route_cards)}):")
        for route_card in self.route_cards:
            print(f"- {route_card.route_name}")
        print()

    def _init_kripke(self):
        """
        Initializer of the Kripke model
        """
        agent_ids = []
        route_card_ids = []
        for agent in self.agents:
            agent_ids.append(agent.agent_id)
        for route_card in self.route_cards:
            route_card_ids.append(route_card.route_name)

        print(f"agent_ids = {agent_ids}")
        self.kripke = TtRKripke(agent_ids=agent_ids, route_cards_ids=route_card_ids)

    def _distribute_route_cards(self):
        """
        Distribute route cards among the agents
        """
        print("Distribute route cards:")
        random.shuffle(self.route_cards)
        step_size = len(self.route_cards) // len(self.agents)
        end = 0
        for agent in self.agents:
            begin = end
            end = begin + step_size
            for card in self.route_cards[begin:end]:
                agent.add_route_card(card)

            self.kripke.update_once_cards_known(agent.agent_id, set(agent.get_route_cards_str()))

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

    def get_true_state(self):
        true_state = {}
        for agent in self.agents:
            route_cards = set([])
            for route_card in agent.own_route_cards:
                route_cards.add(route_card.route_name)
            true_state[agent.agent_id] = route_cards
        return true_state

    def announce_winner(self):
        print("\n------")
        for agent in self.agents:
            for route_card in agent.own_route_cards:
                if not route_card.is_finished:
                    print(f"- Agent {agent.agent_id} did not finish route card {route_card.route_name}: "
                          f"subtracting {route_card.score} points...")
                    agent.score -= route_card.score
        print("\n-----------------------------------------------------------------\n"
              "........................AND THE WINNER IS........................\n"
              "-----------------------------------------------------------------\n")
        points = {}
        for agent in self.agents:
            points[agent.agent_id] = agent.score
            print(f"* Agent {agent.agent_id} has {agent.score} points...")
        agent_winner = max(points.keys(), key=(lambda idx: points[idx]))

        print(f"\nCONGRATULATIONS!!! Agent {agent_winner} has won with {points[agent_winner]} points!\n")
        print(r"""
         _____ _   _   ___   _   _  _   __ _____   ______ ___________   ______ _       _____   _______ _   _ _____    _____ _  ______ 
        |_   _| | | | / _ \ | \ | || | / //  ___|  |  ___|  _  | ___ \  | ___ \ |     / _ \ \ / /_   _| \ | |  __ \  |_   _| | | ___ \
          | | | |_| |/ /_\ \|  \| || |/ / \ `--.   | |_  | | | | |_/ /  | |_/ / |    / /_\ \ V /  | | |  \| | |  \/    | | | |_| |_/ /
          | | |  _  ||  _  || . ` ||    \  `--. \  |  _| | | | |    /   |  __/| |    |  _  |\ /   | | | . ` | | __     | | | __|    / 
          | | | | | || | | || |\  || |\  \/\__/ /  | |   \ \_/ / |\ \   | |   | |____| | | || |  _| |_| |\  | |_\ \    | | | |_| |\ \ 
          \_/ \_| |_/\_| |_/\_| \_/\_| \_/\____/   \_|    \___/\_| \_|  \_|   \_____/\_| |_/\_/  \___/\_| \_/\____/    \_/  \__\_| \_|
        """)
        print(f"Made by Jeroen, Lennard and Sverre!!\n\n")

    def is_finished(self, agent_turn: int) -> bool:
        """
        Function that checks if the game is finished based on
        :return: True if game is finished, else False
        """

        for agent in self.agents:
            # check if an agent has finished all route_cards
            if agent.check_if_route_cards_done():
                print(f"--> AGENT {agent.agent_id} FINISHED ALL ROUTE CARDS")
                return True

        # check if an agent has less than 3 trains left, then everyone has only one turn left
        if self.last_turn is None:
            for agent in self.agents:
                if agent.nr_of_trains < MIN_TRAINS:
                    self.last_turn = agent.agent_id
                    print(f"--> AGENT {agent.agent_id} has less than {MIN_TRAINS}")
        elif agent_turn == self.last_turn:
            print(f"--> AGENT {agent_turn} has played its last turn")
            return True

        # check if all agents could have drawn a card (deck nonempty)
        finished = True
        for agent in self.agents:
            if agent.can_draw_card:
                finished = False
        if finished:
            print(f"--> All agents could not draw any cards since the deck is empty. Game stops.")
        return finished

    def init_game(self, num_agents: int, num_route_cards: int):
        """
        Initializer for the game
        """
        # random.seed(0)

        print("\n--- INITIALIZING TICKET TO RIDE ---\n")
        self.deck = Deck()
        self.board = Board()
        self.agents = []
        self.route_cards = []
        self.turn_num = 0
        self.kripke = None
        self.last_turn = None
        self.in_game = True

        self._init_agents(num_agents)
        self._init_route_cards(num_agents * num_route_cards)
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

        print("\n---- GAME INITIALIZED ---\n")

    def turn(self):
        """
        One turn in the game
        """
        if not self.in_game:
            print("Game already over, skipping turn.")
            return

        print("\n\n----------------------------------------\n"
              "----------------------------------------\n"
              f"--- TURN {self.turn_num}\n"
              "----------------------------------------\n"
              "----------------------------------------\n")

        for agent in self.agents:
            agent.choose_action()
            # agent.print_agent_profile()
            if self.is_finished(agent.agent_id):
                self.in_game = False
                self.announce_winner()
                return

        self.turn_num += 1

    def play(self, num_agents: int, num_route_cards: int):
        """
        Game loop for the Ticket to Ride game
        """
        self.init_game(num_agents, num_route_cards)
        while self.in_game:
            self.turn()
