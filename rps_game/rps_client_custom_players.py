import random
from collections import Counter

from rps_game.rps_client_player import RPSPlayer
from rps_game.rps_config import POSSIBLE_MOVES


class RPSSimpleBotPlayer(RPSPlayer):
    def __init__(self):
        self.name = 'Simple Bot Player'
        self.version = 'v0.1'
        self_id = None

    def __str__(self):
        return f'Client player {self.name} {self.version} {self.id}'

    def initialize(self, id):
        self.id = id
        self.my_biased_moves = POSSIBLE_MOVES.copy()
        move = random.choice(POSSIBLE_MOVES)
        # Play twice as often the move {move}
        self.my_biased_moves += 2 * [move]
        print(self.my_biased_moves)

    def game_result(self, round, player_one_id, player_one_move, player_two_id, player_two_move, winner):
        # winner = -1: draw
        # winner = >0: the player id of the winner
        pass

    def next_move(self, round):
        return random.choice(self.my_biased_moves)

