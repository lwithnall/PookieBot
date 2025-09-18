"""
Test configuration and fixtures for PookieBot tests.
"""

import pytest
import discord
from unittest.mock import MagicMock
import sys
import os

# Add the `pookiebot` package to the sys.path so pytest can discover it
# This is necessary for pytest to find modules within the `pookiebot` directory
# For some more info read:
# https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../pookiebot"))
)

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


@pytest.fixture
def member_factory():
    class MemberFactory:
        def __init__(self):
            self.mem_id = 1000000000

        def create(self):
            mock_member = MagicMock(spec=discord.Member)
            mock_member.id = self.mem_id
            mock_member.name = str(self.mem_id)
            mock_member.mention = f"<@{str(self.mem_id)}>"
            self.mem_id += 1
            return mock_member

    return MemberFactory


@pytest.fixture
def mock_member_list(member_factory):
    return [member_factory.create() for i in range(DEFAULT_MEMBER_LIST_LEN)]


@pytest.fixture
def mock_bank(mock_member_list):
    return Bank(mock_member_list)
