# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
import socket
import pickle

from rps_game.rps_client_player import RPSPlayer
from rps_game.rps_client_my_player import RPSMyPlayer
from rps_game.rps_client_custom_players import *
from rps_game.rps_messages import ClientMsgHello, ServerMsgDuelReadyToStart, \
    ServerMsgRoundStart, ClientMsgRoundMove, ServerMsgRoundResult, \
    ServerMsgExitClient, ClientMsgOK, ServerMsgPrepareForNextRound


def rps_client_main(server_host, server_port, player_class_name):
    # rps_client_player = RPSClientPlayer()
    klass = globals()[player_class_name]
    rps_client_player = klass()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f'Trying to connect to {server_host} on port {server_port} ...')
    # connect to server
    s.connect((server_host, server_port))

    # message you send to server
    message = "Hello from client"

    client_hello = ClientMsgHello(rps_client_player.name, rps_client_player.version)
    data = pickle.dumps(client_hello)

    # msg_exit = MsgExit(0, "test exit")
    # data = pickle.dumps(msg_exit)

    s.send(data)

    # message received from server
    data = s.recv(1024)

    server_msg = pickle.loads(data)
    # print the received message
    # here it would be a reverse of sent message

    print(f'Received from the server : {server_msg}')
    my_id = server_msg.client_id
    print(f'My id is: {my_id}')

    rps_client_player.initialize(my_id)

    # Wait for duel start message
    data = s.recv(1024)
    server_msg = pickle.loads(data)

    assert isinstance(server_msg, ServerMsgDuelReadyToStart)
    print(f'Received from the server : {server_msg}')
    client_OK = ClientMsgOK('Received duel ready to start')
    data = pickle.dumps(client_OK)
    s.send(data)

    game_ended = False
    while not game_ended:
        rdata = s.recv(1024)
        server_msg = pickle.loads(rdata)
        assert isinstance(server_msg, ServerMsgRoundStart)

        round = server_msg.round_num

        print(f'Received from the server : {server_msg}')
        move = rps_client_player.next_move(round)
        msg_move = ClientMsgRoundMove(move)
        data = pickle.dumps(msg_move)
        print(f'Sending to server : {msg_move}')
        s.send(data)

        rdata = s.recv(1024)
        round_result = pickle.loads(rdata)
        assert isinstance(round_result, ServerMsgRoundResult)
        print(f'Result: {round_result.result}')

        client_OK = ClientMsgOK('Received server round result')
        data = pickle.dumps(client_OK)
        s.send(data)

        rps_client_player.game_result(round, round_result.player_one_id, round_result.player_one_move, round_result.player_two_id, round_result.player_two_move, round_result.result)

        rdata = s.recv(1024)
        server_msg = pickle.loads(rdata)
        print(server_msg)

        if isinstance(server_msg, ServerMsgPrepareForNextRound):
            print(f'Preparing for next round: {server_msg.round_num}')
        elif isinstance(server_msg, ServerMsgExitClient):
            print(f'Exit command from server: {server_msg}')
            print(f'Exiting ...')
            game_ended = True
        else:
            raise ("Unexpected server msg type")

    s.close()


