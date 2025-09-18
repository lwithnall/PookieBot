"""
Tests for the Bank class in the gambling module.
"""
import pytest
from pookiebot.cogs.gambling.banking import Bank


class TestBank:
    """Test cases for the Bank class."""

    def test_bank_initialization_single_player(self, mock_member):
        """Test bank initialization with a single player."""
        bank = Bank(mock_member)
        
        assert mock_member in bank
        assert bank.get_player_balance(mock_member) == Bank.INITIAL_BALANCE

    def test_bank_initialization_multiple_players(self, mock_member, mock_member2):
        """Test bank initialization with multiple players."""
        bank = Bank(mock_member, mock_member2)
        
        assert mock_member in bank
        assert mock_member2 in bank
        assert bank.get_player_balance(mock_member) == Bank.INITIAL_BALANCE
        assert bank.get_player_balance(mock_member2) == Bank.INITIAL_BALANCE

    def test_valid_bet_with_sufficient_balance(self, mock_member):
        """Test valid_bet returns True when player has sufficient balance."""
        bank = Bank(mock_member)
        
        assert bank.valid_bet(mock_member, 100) is True
        assert bank.valid_bet(mock_member, Bank.INITIAL_BALANCE) is True

    def test_valid_bet_with_insufficient_balance(self, mock_member):
        """Test valid_bet returns False when player has insufficient balance."""
        bank = Bank(mock_member)
        
        assert bank.valid_bet(mock_member, Bank.INITIAL_BALANCE + 1) is False

    def test_valid_bet_with_zero_or_negative_amount(self, mock_member):
        """Test valid_bet returns False for zero or negative amounts."""
        bank = Bank(mock_member)
        
        assert bank.valid_bet(mock_member, 0) is False
        assert bank.valid_bet(mock_member, -100) is False

    def test_decrease_balance(self, mock_member):
        """Test decreasing player balance."""
        bank = Bank(mock_member)
        initial_balance = bank.get_player_balance(mock_member)
        
        bank.decrease_balance(mock_member, 500)
        
        assert bank.get_player_balance(mock_member) == initial_balance - 500

    def test_increase_balance(self, mock_member):
        """Test increasing player balance."""
        bank = Bank(mock_member)
        initial_balance = bank.get_player_balance(mock_member)
        
        bank.increase_balance(mock_member, 1000)
        
        assert bank.get_player_balance(mock_member) == initial_balance + 1000

    def test_transfer_funds(self, mock_member, mock_member2):
        """Test transferring funds between players."""
        bank = Bank(mock_member, mock_member2)
        transfer_amount = 2000
        
        initial_payer_balance = bank.get_player_balance(mock_member)
        initial_payee_balance = bank.get_player_balance(mock_member2)
        
        bank.transfer_funds(mock_member, mock_member2, transfer_amount)
        
        assert bank.get_player_balance(mock_member) == initial_payer_balance - transfer_amount
        assert bank.get_player_balance(mock_member2) == initial_payee_balance + transfer_amount

    def test_add_player(self, mock_member, mock_member2):
        """Test adding a new player to the bank."""
        bank = Bank(mock_member)
        
        assert mock_member2 not in bank
        
        bank.add_player(mock_member2)
        
        assert mock_member2 in bank
        assert bank.get_player_balance(mock_member2) == Bank.INITIAL_BALANCE

    def test_remove_player(self, mock_member, mock_member2):
        """Test removing a player from the bank."""
        bank = Bank(mock_member, mock_member2)
        
        assert mock_member2 in bank
        
        bank.remove_player(mock_member2)
        
        assert mock_member2 not in bank

    def test_get_balances(self, mock_member, mock_member2):
        """Test getting all player balances."""
        bank = Bank(mock_member, mock_member2)
        
        balances = bank.get_balances()
        
        assert len(balances) == 2
        assert balances[mock_member] == Bank.INITIAL_BALANCE
        assert balances[mock_member2] == Bank.INITIAL_BALANCE

    def test_contains_operator(self, mock_member, mock_member2):
        """Test the __contains__ method (in operator)."""
        bank = Bank(mock_member)
        
        assert mock_member in bank
        assert mock_member2 not in bank

    def test_bank_constants(self):
        """Test that bank constants are set correctly."""
        assert Bank.INITIAL_BALANCE == 10000
        assert Bank.MIN_BALANCE == 0
