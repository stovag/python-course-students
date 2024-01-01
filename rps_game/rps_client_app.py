import os, sys
from datetime import datetime as dt
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
import logging
import argparse

from rps_game.rps_client import rps_client_main
from rps_game.rps_config import RPS_VERSION
from rps_game.rps_config import DEFAULT_SERVER_ADDRESS
from rps_game.rps_config import DEFAULT_SERVER_PORT

# Logger
# logger = logging.getLogger()
logger = logging.getLogger('client' + __name__)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
# streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
streamformat = logging.Formatter('%(process)s %(thread)s:-%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream.setFormatter(streamformat)
logger.addHandler(stream)

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-a", "--Address", type=str, default=DEFAULT_SERVER_ADDRESS, help="Server Address")
parser.add_argument("-p", "--Port", type=int, default=DEFAULT_SERVER_PORT, help="Server Port")
parser.add_argument("-c", "--PlayerClass", type=str, default='RPSMyPlayer', help="Client Player class")
parser.add_argument("-v", "--Verbose", action='store_true', default=False, help="Verbose mode")
parser.add_argument("-t", "--Timeouts", type=float, default=None, help="Socket timeouts")
parser.add_argument("-e", "--ExitServer", action='store_true', default=False, help="Send Exit Message to Server (Terminate the server)")

# Read arguments from command line
args = parser.parse_args()

server_host = args.Address
server_port = args.Port
player_class_name = args.PlayerClass
verbose = args.Verbose
timeouts = args.Timeouts
send_exit = args.ExitServer

# Get timestamp for current run
timestamp = dt.now().strftime("%m%d%Y_%H%M%S")

if verbose:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

# Print info
print(f'RPS Client v{RPS_VERSION} started, {server_host} {server_port} {player_class_name}')
logger.info('Log Info message')

# Run the client
rps_client_main(server_host, server_port, player_class_name, False, logger, timeouts, timestamp, send_exit)
