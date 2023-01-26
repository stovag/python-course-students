import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
import argparse

from rps_game.rps_client import rps_client_main
from rps_game.rps_config import RPS_VERSION

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-a", "--Address", type=str, default='oinoh.ee.duth.gr', help="Server Address")
parser.add_argument("-p", "--Port", type=int, default='4455', help="Server Port")
parser.add_argument("-c", "--PlayerClass", type=str, default='RPSMyPlayer', help="Client Player class")

# Read arguments from command line
args = parser.parse_args()

server_host = args.Address
server_port = args.Port
player_class_name = args.PlayerClass

# Print info
print(f'RPS Client v{RPS_VERSION} starting ...')

# Run the client
rps_client_main(server_host, server_port, player_class_name)
