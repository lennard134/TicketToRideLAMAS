"""
Knowledge base of an agent that holds all knowledge from which possible states can be retrieved
"""

from Agent import Agent
from Game import Game


class KnowledgeBase(object):

    def __init__(self, agent: Agent, game: Game):
        self.game = game
        self.agent = agent
        self.own_route_cards = []
        self.known_route_cards = {}

        self._init_own_route_cards(self.agent)

    def _init_own_route_cards(self, agent: Agent):
        self.own_route_cards = agent.own_route_cards

    def _init_known_route_cards(self):
        for card in self.game.route_cards:
            self.known_route_cards[card.route_name] = self.agent if card.route_name in self.agent.own_route_cards else None
            
