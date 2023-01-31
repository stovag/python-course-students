import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import logging
import argparse
from datetime import datetime

from rps_game.rps_config import RPS_VERSION
from rps_game.rps_config import DEFAULT_SERVER_PORT
from rps_game.rps_server import rps_server_main

# Logger
# logger = logging.getLogger()

logger = logging.getLogger('server'+__name__)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
# streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
# stream.setFormatter(streamformat)
streamformat = logging.Formatter('%(process)s %(thread)s:-%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream.setFormatter(streamformat)
logger.addHandler(stream)

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--Port", type=int, default=DEFAULT_SERVER_PORT, help="Server Listener Port")
parser.add_argument("-r", "--Rounds", type=int, default=5, help="Number of game rounds")
parser.add_argument("-t", "--Timeouts", type=float, default=None, help="Socket timeouts")
parser.add_argument("-b", "--Bot", action='store_true', default=False, help="Clients play against bot")
parser.add_argument("-v", "--Verbose", action='store_true', default=False, help="Verbose mode")
parser.add_argument("-c", "--PlayerClass", type=str, default='RPSSimpleBotPlayer', help="Client player class for bot (for bot mode of server)")

# Read arguments from command line
args = parser.parse_args()

server_port = args.Port
game_rounds = args.Rounds
clients_play_against_bot = args.Bot
player_class_name = args.PlayerClass
verbose = args.Verbose
timeouts = args.Timeouts

if verbose:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

print(datetime.now())
server_name = "Python MSc Course"

print(f'RPS Server {server_name} v{RPS_VERSION} started, {server_port} {game_rounds} {clients_play_against_bot} {player_class_name}')
logger.info(f'Logging info message')

rps_server_main(server_name, server_port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts)
