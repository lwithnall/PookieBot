import pytest
from cogs.gambling.banking import Bank
from cogs.gambling.games import (
    Game,
    CardGame,
    Poker,
    BlackJack,
    Roulette,
)
from cogs.gambling.session import GamblingSession

DEFAULT_MEMBER_LIST_LEN = 10


def test_bank(member_factory):
    member_list = [member_factory.get() for i in range(DEFAULT_MEMBER_LIST_LEN)]
    bank = Bank(*member_list)
