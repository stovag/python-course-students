import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import argparse

from rps_game.rps_config import RPS_VERSION
from rps_game.rps_server import rps_server_main

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--Port", type=int, default='4455', help="Server Listener Port")
parser.add_argument("-r", "--Rounds", type=int, default=5, help="Number of game rounds")
parser.add_argument("-b", "--Bot", action='store_true', default=False, help="Clients play against bot")
parser.add_argument("-c", "--PlayerClass", type=str, default='RPSSimpleBotPlayer', help="Client player class for bot (for bot mode of server)")

# Read arguments from command line
args = parser.parse_args()

server_port = args.Port
game_rounds = args.Rounds
clients_play_against_bot = args.Bot
player_class_name = args.PlayerClass

server_name = "Python MSc Course"

print(f'RPS Server {server_name} v{RPS_VERSION} starting ...')

rps_server_main(server_name, server_port, clients_play_against_bot, player_class_name, game_rounds)
