import random

from rps_game.rps_config import POSSIBLE_MOVES


class RPSPlayer:
    def __init__(self):
        self.name = 'Demo Player'
        self.version = 'v0.1'
        self_id = None

    def __str__(self):
        return f'Client player {self.name} {self.version} {self.id}'

    def initialize(self, id):
        self.id = id

    def game_result(self, round, player_one_id, player_one_move, player_two_id, player_two_move, winner):
        # winner = -1: draw
        # winner = >0: the player id of the winner
        pass

    def next_move(self, round):
        return random.choice(POSSIBLE_MOVES)