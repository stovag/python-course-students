# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
import argparse

from rps_client import rps_client_main

# Initialize parser
parser = argparse.ArgumentParser()
parser.parse_args()

# Adding optional argument
parser.add_argument("-a", "--Address", type=str, default='oinoh.ee.duth.gr', help="Server Address")
parser.add_argument("-p", "--Port", type=int, default='4455', help="Server Port")

# Read arguments from command line
args = parser.parse_args()

server_host = args.Address
server_port = args.Port

# client_name = "Oinoh"
# client_version = "0.2"

rps_client_main(server_host, server_port)
