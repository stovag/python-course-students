import random

import pandas as pd

from rps_game.rps_client_player import RPSPlayer
from rps_game.rps_config import POSSIBLE_MOVES


class RPSMyPlayer(RPSPlayer):
    def __init__(self):
        self.name = 'My Player'
        self.version = 'v0.1'
        self.loses_from = {
            "paper": "scissors",
            "scissors": "rock",
            "rock": "paper"
        }
        self_id = None
        self.timestamp = None
        self.opponent_moves = []


    def __str__(self):
        return f'Client player {self.name} {self.version} {self.id}'

    def initialize(self, id, timestamp):
        # Set timestamp from client ts
        self.timestamp = timestamp
        self.id = id

    def game_result(self, round, player_one_id, player_one_move, player_two_id, player_two_move, winner):
        # winner = -1: draw
        # winner = >0: the player id of the winner
        pass

    def next_move(self, round):
        bias = self.get_bot_bias()
        if bias is not None:
            bias = bias.sort_values(ascending=False)
            # print(bias[0])
            if max(bias) > 50:
                for choice in POSSIBLE_MOVES:
                    # If a move shows up more than 50% -> select its counter
                    if bias[choice] == max(bias):
                        usual_choice = choice
                        return self.loses_from[usual_choice]
            else:
                # If no obvious move bias, pick a move based on frequencies
                choice = random.choices(bias.index, weights=bias,k=1)[0]
                return self.loses_from[choice]
            
        else:
            # Get random move
            return random.choice(POSSIBLE_MOVES)
    
    # Calculate the frequency of each move from the bot from current logs
    def get_bot_bias(self):
        rounds_df = pd.read_csv(f"logs/result_log_{self.timestamp}.csv")
        if len(rounds_df) >= 25:
            df = rounds_df.tail(25)
            bot_choices = df['b_choice'].value_counts(normalize=True) * 100
            # Check if any movces are missing eg: the bot didn't make any rock moves in the last 25 rounds. 
            # Add it to value_count if needed
            for move in POSSIBLE_MOVES:
                if move not in bot_choices.index:
                    bot_choices._set_value(move, 0)
            return bot_choices
        return None