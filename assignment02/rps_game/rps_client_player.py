import random

class RPSClientPlayer:
    def __init__(self):
        self.name = 'Demo Player'
        self.version = 'v0.1'

    def __str__(self):
        return f'Client player {self.name} {self.version}'

    def game_result(self, round, player1_move, player2_move, winner):
        # winner = 1: player 1 won
        # winner = 2: player 2 won
        # winner = 0: draw
        pass

    def next_move(self, round):
        return random.choice(['rock', 'paper', 'scissors'])