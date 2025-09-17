"""
Bank class to manage user balances for game sessions.
"""

import discord


class Bank:
    INITIAL_BALANCE = 10000
    MIN_BALANCE = 0

    def __init__(self, *players: discord.Member):
        self._balances = {player: self.INITIAL_BALANCE for player in players}

    def __contains__(self, player: discord.Member):
        return player in self._balances

    def valid_bet(self, player: discord.Member, amount: int):
        """
        Return if bet amount is valid.
        i.e. 0 < amount < player balance
        """
        if amount <= 0 or amount > self._balances[player]:
            return False

        return True

    def decrease_balance(self, player: discord.Member, amount: int):
        """Subtract amount from player's balance"""
        self._balances[player] -= amount

    def increase_balance(self, player: discord.Member, amount: int):
        """Add money to players account"""
        self._balances[player] += amount

    def transfer_funds(self, payer: discord.Member, payee: discord.Member, amount: int):
        """Transfer amount from payer to payee"""
        self._balances[payer] -= amount
        self._balances[payee] += amount

    def add_player(self, player: discord.Member):
        """Add player to bank with initial balance"""
        self._balances[player] = self.INITIAL_BALANCE

    def remove_player(self, player: discord.Member):
        """Remove player from bank"""
        del self._balances[player]

    def get_player_balance(self, player: discord.Member):
        """Return the balance of given player"""
        return self._balances[player]

    def get_balances(self):
        """Return player balances"""
        return self._balances
