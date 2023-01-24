# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
import socket
import pickle

from rps_client_player import RPSClientPlayer
from rps_messages import ClientMsgHello, ServerMsgDuelReadyToStart, \
    ServerMsgRoundStart, ClientMsgRoundMove, ServerMsgRoundResult, \
    ServerMsgExitClient, ClientMsgOK, ServerMsgPrepareForNextRound


def rps_client_main(server_host, server_port):
    rps_client_player = RPSClientPlayer()

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

    # s.send(client_name.encode())
    #
    # data = s.recv(1024)
    # client_id = int(data.decode())
    #
    # print(f'{client_id}')

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
        server_msg = pickle.loads(rdata)
        assert isinstance(server_msg, ServerMsgRoundResult)
        print(f'Result: {server_msg.result}')

        client_OK = ClientMsgOK('Received server round result')
        data = pickle.dumps(client_OK)
        s.send(data)

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


