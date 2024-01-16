import random

import pandas as pd

from rps_game.rps_client_player import RPSPlayer
from rps_game.rps_config import POSSIBLE_MOVES


class RPSMyAdaptivePlayer(RPSPlayer):
    """
    A Rock-Paper-Scissors player implementing adaptive strategies.

    This player class adapts its strategy based on the 
    frequency of its opponent's recorded in recent game rounds.
    It starts with random moves for the first n rounds 
    and then adjusts its strategy based on observed biases.

    Attributes:
    - name (str): The name of the player.
    - version (str): The version of the player.
    - counter_moves (dict): A dictionary mapping each possible move to its counter-move.
    - self_id (int): The player's unique identifier.
    - opponent_moves (list): A list to store the opponent's moves.
    - current_bias (str): The move that the player currently biases towards.
    - bias_high_limit (int): The threshold for considering a bias as high, used in move selection.
    - bias_low_limit (int): The threshold for considering a bias as low, used in move selection.
    - window (int): The number of recent game rounds used to calculate bias.
    
    Methods:
    - __init__(): Initializes the player with default values and counter-move dictionary.
    - __str__(): Returns a string representation of the player.
    - initialize(id): Initializes the player with a unique identifier.
    - game_result(round, player_one_id, player_one_move, player_two_id, player_two_move, winner):
        Updates the player's internal state based on the outcome of the game round.
    - next_move(round): Determines the player's next move based on observed biases or random selection.
    - get_bot_bias(): Calculates the frequency of each move from the player's recent game rounds.

    """
    def __init__(self):
        self.name = 'My Adaptive Player'
        self.version = 'v0.1'
        # Initialize counter_move dictionary
        self.counter_moves = {
            "paper": "scissors",
            "scissors": "rock",
            "rock": "paper"
        }
        self_id = None
        self.opponent_moves = []
        self.current_bias = None
        self.bias_high_limit = 40
        self.bias_low_limit = 15
        self.window = 15


    def __str__(self):
        return f'Client player {self.name} {self.version} {self.id}'

    def initialize(self, id):
        self.id = id

    def game_result(self, round, player_one_id, player_one_move, player_two_id, player_two_move, winner):
        # winner = -1: draw
        # winner = >0: the player id of the winner
        pass

    def next_move(self, round):
        """
        Determine the player's next move based on observed biases or random selection.

        Args:
        - round (int): The current round of the game.

        Returns:
        - str: The selected move for the current round.

        Note:
        This method uses the frequency bias calculated from the player's recent game rounds to adjust its strategy.
        If a move shows up more than `bias_high_limit`%, the player selects its counter move.
        If no moves have a frequency greater than or equal to `bias_high_limit`, the player checks for bias changes.
        If bias changes are detected (minimum bias below `bias_low_limit` and not the maximum bias), the player adjusts its strategy.
        If no obvious bias is detected, the player picks a move based on frequencies.
        For the first 25 rounds, the player selects random moves.

        Example:
        >>> player = RPSMyAdaptivePlayer()
        >>> player.next_move(30)
        """
        
        bias = self.get_bot_bias()
        if bias is not None:
            # If a move shows up more than 50% -> select its counter move
            if max(bias) >= self.bias_high_limit:
                for choice in POSSIBLE_MOVES:
                    if bias[choice] == max(bias):
                        self.current_bias = choice
                        return self.counter_moves[self.current_bias]
            # If no moves with freq >= 50% check if bias has changed. When changing the minimum bias will be extremely low 
            elif min(bias) <= self.bias_low_limit:
                for choice in POSSIBLE_MOVES:
                    if bias[choice] != min(bias) and bias[choice] != max(bias):
                        self.current_bias = choice
                        return self.counter_moves[self.current_bias]
            else:
                # If no obvious bias is detected, pick a move based on frequencies
                choice = random.choices(bias.index, weights=bias,k=1)[0]
                return self.counter_moves[choice]
        #For the first 25 rounds pick random moves
        else:
            # Get random move
            return random.choice(POSSIBLE_MOVES)
    
    # Calculate the frequency of each move from the bot from current logs
    def get_bot_bias(self):
        """
        Calculate the frequency of each move from the player's recent game rounds.

        Returns:
        - pandas.Series: A Series containing move frequencies as percentages.

        Note:
        This method assumes the existence of a constant POSSIBLE_MOVES list and requires external game log data
        stored in a 'logs/result_log.csv' file. The calculation considers the last `window` rounds of the log.

        Example:
        >>> player = RPSMyAdaptivePlayer()
        >>> player.get_bot_bias()
        """
        rounds_df = pd.read_csv(f"logs/result_log.csv").tail(self.window)
        bot_choices = rounds_df['b_choice'].value_counts(normalize=True) * 100
        # Check if any movces are missing eg: the bot didn't make any rock moves in the last 25 rounds.
        # Add it to value_count if needed
        for move in POSSIBLE_MOVES:
            if move not in bot_choices.index:
                bot_choices._set_value(move, 0)
        return bot_choices
