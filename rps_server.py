# Server sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

# import socket programming library
import socket
import pickle

# import thread module
import threading

import argparse

from rps_client import rps_client_main
from rps_messages import ServerMsgHello, ClientMsgHello, ServerMsgExitClient
from rps_server_worker import serve_duel

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--Port", type=int, default='4455', help="Server Listener Port")
parser.add_argument("-r", "--Rounds", type=int, default=5, help="Number of game rounds")
parser.add_argument("-b", "--Bot", action='store_true', default=False, help="Clients play against bot")

# Read arguments from command line
args = parser.parse_args()

game_rounds = args.Rounds

print_lock = threading.Lock()

host = ""

server_name = "Python MSc Course"

client_id = 0

clients_play_against_bot = args.Bot

class Client:
    def __init__(self, name, client_id, socket):
        self.name = name
        self.client_id = client_id
        self.socket = socket

    def __str__(self):
        return f'Client: {self.name}, {self.client_id}'


# reserve a port on your computer
# in our case it is 12345 but it
# can be anything

port = args.Port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("socket binded to port", port)

# put the socket into listening mode
s.listen(5)
print("Server socket is listening")

client_list = []

# a forever loop until client wants to exit
while True:
    # establish connection with client
    c, addr = s.accept()

    # lock acquired by client
    print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])
    print_lock.release()

    data = c.recv(1024)
    # client_name = c.recv(1024)
    client_msg = pickle.loads(data)

    if isinstance(client_msg, ClientMsgHello):
        print_lock.acquire()
        print(f'Message from client: {client_msg}')
        # print(f'Data from client: {data.decode()}')
        print_lock.release()
        # Sending the client id
        srv_msg = ServerMsgHello(server_name, client_id)
        data = pickle.dumps(srv_msg)
        c.send(data)

        client_id += 1

        client = Client(client_msg.name, client_id, c)
        client_list.append(client)

        if clients_play_against_bot:
            if len(client_list)==1:
                client_bot = threading.Thread(target=rps_client_main, args=('127.0.0.1', port))
                client_bot.start()
        # exit_msg = MsgClientExit(0, "test exit")
        # data = pickle.dumps(exit_msg)
        # c.send(data)

    elif isinstance(client_msg, ServerMsgExitClient):
        print_lock.acquire()
        print(f'Message from client: {client_msg}')
        # print(f'Data from client: {data.decode()}')
        print(f'Server terminating ...')
        print_lock.release()
        break

    else:
        print(f'Unexpected message type from client: {client_msg}')
        print(f'Ignoring the connection.')

    if len(client_list) == 2:
        duel_client_list = client_list[0:2]
        client_list = client_list[2:]
        # serve_duel(duel_client_list)
        server_worker = threading.Thread(target=serve_duel, args=(duel_client_list, game_rounds))
        server_worker.start()

    # srv_msg = "You are connected to the server!"
    # c.send(srv_msg.encode())
    #
    # data = c.recv(1024)
    # client_name = data.decode()
    # print_lock.acquire()
    # print(f'{client_name=}')
    # print_lock.release()

s.close()
