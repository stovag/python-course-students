# Server sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

# import socket programming library
import socket
import pickle
import sys

# import thread module
import threading

from rps_game.rps_client import rps_client_main
from rps_game.rps_config import RPS_VERSION
from rps_game.rps_messages import ServerMsgHello, ClientMsgHello, ServerMsgExitClient, ClientMsgExitServer, \
    ServerMsgRejectClientConnection
from rps_server_worker import serve_duel

host = ""
client_id = 0
# print_lock = threading.Lock()
exit_flag_lock = threading.Lock()
exit_flag = False
client_list_lock = threading.Lock()

class Client:
    def __init__(self, name, client_id, socket, i_am_a_bot = False):
        self.name = name
        self.client_id = client_id
        self.socket = socket
        self.i_am_a_bot = i_am_a_bot

    def __str__(self):
        return f'Client: {self.name}, {self.client_id}, {self.i_am_a_bot}'


# reserve a port on your computer
# in our case it is 12345 but it
# can be anything

def serve_new_client_connection(c, client_id, client_list, client_bot_list, server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts):
    data = c.recv(1024)
    # client_name = c.recv(1024)
    client_msg = pickle.loads(data)

    if isinstance(client_msg, ClientMsgHello):
        logger.info(f'Message from client: {client_msg}')

        # Check client qualifications
        server_app_version = RPS_VERSION
        client_app_version = client_msg.client_app_version
        if server_app_version != client_app_version:
            # Incompatible client version, the client connection is rejected
            srv_msg = ServerMsgRejectClientConnection(server_name, server_app_version, f'Client rps version ({client_app_version}) incompatible with server version ({server_app_version})')
            data = pickle.dumps(srv_msg)
            c.send(data)
        else:
            # The client has been accepted
            # Sending the client id
            srv_msg = ServerMsgHello(server_name, RPS_VERSION, client_id)
            data = pickle.dumps(srv_msg)
            c.send(data)

            client = Client(client_msg.name, client_id, c, client_msg.i_am_a_bot)
            with client_list_lock:
                if client_msg.i_am_a_bot:
                    client_bot_list.append(client)
                else:
                    client_list.append(client)
                client_id += 1

            # exit_msg = MsgClientExit(0, "test exit")
            # data = pickle.dumps(exit_msg)
            # c.send(data)
            rps_server_create_duel(c, client_id, client_list, client_bot_list, server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts)

    elif isinstance(client_msg, ClientMsgExitServer):
        logger.info(f'Message from client: {client_msg}')
        # print(f'Data from client: {data.decode()}')
        global exit_flag
        with exit_flag_lock:
            exit_flag = True
        logger.info(f'Setting Server termination flag ...')
        logger.info(f'Exiting ...')
        sys.exit(0)
    else:
        logger.error(f'Unexpected message type from client: {client_msg}')
        logger.error(f'Ignoring the connection.')

def rps_server_create_duel(c, client_id, client_list, client_bot_list, server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts):
    if clients_play_against_bot:
        # Each client plays against a bot client
        if len(client_list) >= 1:
            if len(client_bot_list) >= 1:
                duel_client_list = []
                duel_client_list.append(client_list.pop())
                duel_client_list.append(client_bot_list.pop())
                # serve_duel(duel_client_list, game_rounds, logger)
                server_worker = threading.Thread(target=serve_duel, args=(duel_client_list, game_rounds, logger))
                server_worker.start()
            else:
                client_bot = threading.Thread(target=rps_client_main, args=('127.0.0.1', port, player_class_name, True, logger, timeouts))
                client_bot.start()
    else:
        # Clients play in duels
        if len(client_list) >= 2:
            duel_client_list = []
            duel_client_list.append(client_list.pop())
            duel_client_list.append(client_list.pop())
            # serve_duel(duel_client_list, game_rounds, logger)
            server_worker = threading.Thread(target=serve_duel, args=(duel_client_list, game_rounds, logger))
            server_worker.start()


def rps_server_main(server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts):
    global exit_flag
    with exit_flag_lock:
        exit_flag = False
    logger.info(f'RPS server bot mode: {clients_play_against_bot}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s.bind((host, port))
    logger.info("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    logger.info("Server socket is listening")

    client_list = [] # For normal clients
    client_bot_list = [] # For clients that are bots created by the server

    global client_id
    client_id = 0

    # a forever loop until client wants to exit
    while True:
        try:
            # check if the main thread should terminate
            with exit_flag_lock:
                if exit_flag:
                    break

            # establish connection with client
            c, addr = s.accept()
            c.settimeout(timeouts)

            # lock acquired by client
            logger.info('Connected to :', addr[0], ':', addr[1])

            # serve_new_client_connection( c, client_id, client_list, client_bot_list, server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts)
            server_new_connection_thread = threading.Thread(target=serve_new_client_connection, args=(c, client_id, client_list, client_bot_list, server_name, port, clients_play_against_bot, player_class_name, game_rounds, logger, timeouts))
            client_id += 1
            server_new_connection_thread.start()
        except socket.timeout:
            # Simply continue ... (and check the exit_flag)
            pass
    s.close()
