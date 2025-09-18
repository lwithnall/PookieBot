"""
Test configuration and fixtures for PookieBot tests.
"""

import pytest
import discord
import random

random.seed(123)

@pytest.fixture
def member_factory():
    mock_member = 

# """
# Test configuration and fixtures for PookieBot tests.
# """
# import pytest
# import discord
# from discord.ext import commands
# from unittest.mock import AsyncMock, MagicMock


# @pytest.fixture
# def mock_bot():
#     """Create a mock Discord bot for testing."""
#     bot = MagicMock(spec=commands.Bot)
#     bot.user = MagicMock()
#     bot.user.name = "PookieBot"
#     bot.user.id = 123456789
#     return bot


# @pytest.fixture
# def mock_member():
#     """Create a mock Discord member for testing."""
#     member = MagicMock(spec=discord.Member)
#     member.id = 987654321
#     member.name = "TestUser"
#     member.mention = "<@987654321>"
#     return member


# @pytest.fixture
# def mock_member2():
#     """Create a second mock Discord member for testing."""
#     member = MagicMock(spec=discord.Member)
#     member.id = 111222333
#     member.name = "TestUser2"
#     member.mention = "<@111222333>"
#     return member


# @pytest.fixture
# def mock_ctx(mock_bot, mock_member):
#     """Create a mock Discord context for testing commands."""
#     ctx = MagicMock(spec=commands.Context)
#     ctx.bot = mock_bot
#     ctx.author = mock_member
#     ctx.send = AsyncMock()
#     ctx.command = MagicMock()
#     ctx.command.name = "test_command"
#     return ctx
