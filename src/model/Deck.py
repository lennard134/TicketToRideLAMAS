"""
This class represents the deck of playing cards with coloured wagons and locomotives
"""
import random
from src.model import config

# Config in Deck Config
NR_COLOUR_CARDS = config.DECK_CONFIG['NR_COLOUR_CARDS']
NR_JOKERS = config.DECK_CONFIG['NR_JOKERS']
NR_OPEN_CARDS = config.DECK_CONFIG['NR_OPEN_CARDS']
TRAIN_COLOURS = config.DECK_CONFIG['TRAIN_COLOURS']
JOKER_COLOUR = config.DECK_CONFIG['JOKER_COLOUR']


class Deck(object):
    def __init__(self):
        self.closed_cards = []
        self.open_cards = []
        self.used_cards = []
        self._init_cards()

    def _init_cards(self):
        """
        Function to initialize a new deck of playing cards
        """
        deck = []
        for colour in TRAIN_COLOURS:
            deck.extend(NR_COLOUR_CARDS * [colour])

        deck.extend(NR_JOKERS * [JOKER_COLOUR])

        random.shuffle(deck)
        self.closed_cards = deck
        while len(self.open_cards) < NR_OPEN_CARDS:
            self.open_cards.append(self.remove_closed_card())

    def remove_open_card(self, colour: str):
        """
        Remove a card from the open deck
        """
        assert colour in self.open_cards, "COLOUR NOT IN OPEN CARD"

        self.open_cards.remove(colour)
        self.open_cards.append(self.remove_closed_card())

    def remove_closed_card(self):
        """
        Remove a card from the closed deck
        :return: Returns closed card from deck
        """
        if not self.closed_cards and self.used_cards:  # No closed cards
            self.shuffle_used_cards()
        elif not self.closed_cards:
            if self.open_cards:
                return self.open_cards.pop()
            return None

        return self.closed_cards.pop()

    def play_train_cards(self, train_cards: list[str]):
        """
        Add the played train cards to the used cards stack
        """
        self.used_cards.extend(train_cards)

    def shuffle_used_cards(self):
        """
        Gets called if closed card deck is empty and shuffles the played cards
        """
        self.closed_cards.extend(self.used_cards)
        random.shuffle(self.closed_cards)
        self.used_cards = []
        while len(self.open_cards) < NR_OPEN_CARDS:  # add to open cards if less than NR_OPEN_CARDS
            self.open_cards.append(self.remove_closed_card())

