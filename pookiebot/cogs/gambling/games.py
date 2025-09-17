import discord
from .banking import Bank
from random import shuffle, choice

# Map cards suits to their unicode symbols
SUITS = {
    "spades": "\u2660",
    "hearts": "\u2665",
    "clubs": "\u2663",
    "diamonds": "\u25C6"}

# Get set of all card ranks
RANKS = {str(x) for x in range(2, 10)}.union(set("JQKA"))

# Type hints for card games
type Card = (str, str) # (suit, rank)
type Deck = list[Card]

async def message_player(player: discord.Member, message: str):
    channel = await player.create_dm()
    await channel.send(message)

class Game:
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        self._bank = bank
        self._players = players

class CardGame(Game):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
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
        if self.deck_empty():
            self.deck = self.discards
            self.discards = set()
            self.shuffle_deck()
        return self.deck.pop()

    def discard(self, player: discord.Member, card: Card) -> None:
        self.hands[player].remove(card)
        self.discards.add(card)

    def deal(self, handsize: int) -> None:
        hands = {}
        for player in self._players:
            hand = {self.pop_card() for _ in range(handsize)}
            hands[player] = hand
        self.hands = hands

class Poker(CardGame):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        super().__init__(bank, players)
    
    def main(self):
        ...

class BlackJack(CardGame):
    def __init__(self, bank: Bank, players: list[discord.Member]) -> None:
        super().__init__(bank, players)

class Roulette(Game):
    ...