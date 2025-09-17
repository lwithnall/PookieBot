from typing import Optional
from functools import wraps
import discord
from discord.ext import commands
from .banking import Bank
from .games import Poker, BlackJack, Roulette
from utils.chat_formatter import heading

# GAMES = {"poker", "blackjack", "roulette"}


# def valid_game(game: str):
#     return game in GAMES


def session_game(func):
    """
    Wrapper to check if game can start.
    Gambling games should only begin if:
    - Session is in progress
    - No other gambling game is running
    """
    @wraps(func)
    async def decorate_wrapper(self, ctx, *args, **kwargs):
        if not self._active:
            return await ctx.send("No gambling session currently running. Start one using the 'gamble' command.")
        if self._current_game:
            return await ctx.send("Game already in progress.")
        return await func(self, ctx, *args, **kwargs)
    return decorate_wrapper

def requires_session(func):
    """
    Wrapper for basic commands interacting with the session (e.g. joining, starting)
    Checks if a session is running.
    """
    @wraps(func)
    async def decorate_wrapper(self, ctx, *args, **kwargs):
        if not self._active:
            return await ctx.send("No gambling session currently running. Start one using the 'gamble' command.")
        return await func(self, ctx, *args, **kwargs)
    return decorate_wrapper


class GamblingSession(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bank = None
        self._active = False
        self._current_game = None

    @commands.command(name="gamble")
    async def start_session(self, ctx, *players: discord.Member):
        """Begin gambling session with provided players."""
        if self._active:
            return await ctx.send("Session already in progress.")
        if len(players) < 2:
            return await ctx.send("Must have 2 or more participants.")

        self.bank = Bank(*players)
        self._active = True
        self._current_game = None

        players_str = ", ".join([player.display_name for player in players])
        return await ctx.send(f"Session has begun!! Players are {players_str}.")

    @commands.command(name="quit")
    @requires_session
    async def terminate_session(self, ctx):
        """Terminate current gambling session."""
        self._active = False
        self._current_game = None
        self.bank = None
        return await ctx.send("Ending session. Thanks for playing.")

    @commands.command()
    @requires_session
    async def join(self, ctx):
        """Join the current gambling session if one is running."""
        author = ctx.author
        if author in self.bank:
            return await ctx.send(f"Hi {author.display_name}, you're already in the session.")
        self.bank.add_player(author)
        return await ctx.send(f"{author.display_name} has joined the session!")

    @commands.command()
    @requires_session
    async def leave(self, ctx):
        """Leave the current gambling session if one is running"""
        author = ctx.author
        if author not in self.bank:
            return await ctx.send(f"Hi {author.display_name}, you're not in the current session.")

        self.bank.remove_player(author)
        return await ctx.send(f"{author.display_name} has left the session </3")

    @commands.command()
    @requires_session
    async def scoreboard(self, ctx):
        """
        If session is currently running print players with their current balances.
        Players are balanced in descending order by balance.
        Example format -
            1. player1: 100
            2. plyaer2: 99
            3. player0: 0
        """
        # Get player balances
        # Balance dictionary converted to tuple array using .items()    
        # Format [(player1, money), (player2, money), ...]
        balances = self.bank.get_balances().items()

        # Sort by money (descending order)
        balances = sorted(balances, key=lambda item: item[1], reverse=True)

        leaderboard = f"{heading("Leaderboard", 3)}\n"
        for num, (player, money) in enumerate(balances):
            # Convert 0-index to 1-index
            leaderboard += f"{num+1}. {player.display_name}: ${money:,}\n"
        await ctx.send(leaderboard)

    @commands.command()
    @session_game
    async def poker(self, ctx, *players: Optional[discord.Member]):
        self._current_game = "poker"

    @commands.command()
    @session_game
    async def blackjack(self, ctx, *players: Optional[discord.Member]): ...

    @commands.command()
    @session_game
    async def roulette(self, ctx, *players: Optional[discord.Member]): ...

async def setup(bot: commands.Bot):
    await bot.add_cog(GamblingSession(bot=bot))