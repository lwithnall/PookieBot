import discord
from random import shuffle, choice
from .banking import Bank
from utils.dm_messaging import message_user

# Map cards suits to their unicode symbols
SUITS = {
    "spades": "\u2660",
    "hearts": "\u2665",
    "clubs": "\u2663",
    "diamonds": "\u25c6",
}

# Get set of all card ranks
RANKS = {str(x) for x in range(2, 10)}.union(set("JQKA"))

# Type hints for card games
Card = tuple[str, str]  # (suit, rank)
Deck = list[Card]


class Game:
    """Default game class storing bank and active player details."""

    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        """
        Initiate instance of a game

        Parameters
        bank: Bank - the bank instance for the session
        players: list[discord.Member] - list of players included,
            NOTE: not every player registered in the bank needs to be included in this list
        """
        self._bank = bank
        self._players = players


class CardGame(Game):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        """
        Initiate card game instance.
        Deck contains typical 52 cards with 
        - suits: spades, hearts, clubs, diamonds
        - ranks: A, 2-10, J, Q, K
        Deck is shuffled on start-up

        Discards represents cards not in players hands nor in the deck
        """
        super().__init__(bank, players)
        self.deck = CardGame.get_base_deck()
        self.shuffle_deck()
        self.discards = set()
        self.hands = None

    @classmethod
    def get_base_deck() -> Deck:
        """Return card deck. Returned as list since order matters"""
        return [(suit, rank) for suit in SUITS for rank in RANKS]

    @classmethod
    def get_random_card() -> Card:
        suit = choice(SUITS)
        rank = choice(RANKS)
        return (suit, rank)

    def shuffle_deck(self) -> None:
        """Shuffle the stored deck in place"""
        shuffle(self.deck)

    def deck_empty(self) -> bool:
        return len(self.deck) <= 0

    def pop_card(self) -> Card:
        """Pop card from top of deck array. If deck is empty shuffle discards back into it, then draw."""
        if self.deck_empty():
            self.deck = self.discards
            self.discards = set()
            self.shuffle_deck()
        return self.deck.pop()

    def discard(self, player: discord.Member, card: Card) -> None:
        """
        Remove card from players hand and add it to the discard pile.
        
        Parameters
        player: discord.Member - the player who is discarding a card
        card: Card - the card being discarded from players hand
        """
        self.hands[player].remove(card)
        self.discards.add(card)

    def deal(self, handsize: int) -> None:
        """
        'Deal' cards from the deck into players hands
        
        Parameters
        handsize: int - the number of cards each player can hold
        """
        hands = {}
        for player in self._players:
            hand = {self.pop_card() for _ in range(handsize)}
            hands[player] = hand
        self.hands = hands


class Poker(CardGame):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        super().__init__(bank, players)

    def main(self): ...


class BlackJack(CardGame):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        super().__init__(bank, players)

class Roulette(Game):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        super().__init__(bank, players)
    