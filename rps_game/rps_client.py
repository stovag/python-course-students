# Client sketch from
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
import socket
import pickle
from datetime import datetime as dt

import pandas as pd

from rps_game.rps_client_player import RPSPlayer
from rps_game.rps_client_my_player import *
from rps_game.rps_client_custom_players import *
from rps_game.rps_client_adaptive_player import *
from rps_game.rps_config import RPS_VERSION
from rps_game.rps_messages import (
    ClientMsgHello,
    ServerMsgDuelReadyToStart,
    ServerMsgRoundStart,
    ClientMsgRoundMove,
    ServerMsgRoundResult,
    ServerMsgExitClient,
    ClientMsgOK,
    ServerMsgPrepareForNextRound,
    ClientMsgExitServer,
    ServerMsgRejectClientConnection,
    ServerMsgHello,
)


def rps_client_main(
    server_host,
    server_port,
    player_class_name,
    i_am_a_bot,
    logger,
    timeouts,
    send_server_exit_msg=False,
):
    # rps_client_player = RPSClientPlayer()
    klass = globals()[player_class_name]
    rps_client_player = klass()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logger.info(f"Trying to connect to {server_host} on port {server_port} ...")
    # connect to server
    s.connect((server_host, server_port))
    s.settimeout(timeouts)

    # message you send to server
    message = "Hello from client"

    # Initialize log file for current run
    logging_dict = {
        "p_choice": [],
        "b_choice": [],
        "result": [],
        "server_host": [],
        "server_port": [],
        "player_class_name": [],
        "i_am_a_bot": [],
        "id": []
    }
    if player_class_name != "RPSSimpleBotPlayer":
        df_logs = pd.DataFrame.from_dict(logging_dict)
        df_logs.to_csv(f"logs/result_log.csv", mode="w", index=False)


    if send_server_exit_msg:
        print(f"Sending exit message to server {server_host} {server_port}")
        send_exit = ClientMsgExitServer(
            f"Exit message from client {rps_client_player.name}", 0
        )
        data = pickle.dumps(send_exit)
        s.send(data)
    else:
        client_hello = ClientMsgHello(
            rps_client_player.name, rps_client_player.version, i_am_a_bot, RPS_VERSION
        )
        data = pickle.dumps(client_hello)

        # msg_exit = MsgExit(0, "test exit")
        # data = pickle.dumps(msg_exit)

        s.send(data)

        # message received from server
        data = s.recv(1024)
        server_msg = pickle.loads(data)
        # print the received message
        # here it would be a reverse of sent message

        logger.info(f"Received from the server : {server_msg}")

        if isinstance(server_msg, ServerMsgRejectClientConnection):
            logger.error(f"Connection rejected by server with msg: {server_msg.msg}")
        else:
            assert isinstance(server_msg, ServerMsgHello)
            my_id = server_msg.client_id
            logger.info(f"My id is: {my_id}")
            print(f"My id is: {my_id}")
            rps_client_player.initialize(my_id)

            # Wait for duel start message
            data = s.recv(1024)
            server_msg = pickle.loads(data)

            assert isinstance(server_msg, ServerMsgDuelReadyToStart)
            logger.info(f"Received from the server : {server_msg}")
            client_OK = ClientMsgOK("Received duel ready to start")
            data = pickle.dumps(client_OK)
            s.send(data)

            game_ended = False
            game_rounds_counter = 0
            while not game_ended:
                logger.info(f"Waiting for round start from server")
                rdata = s.recv(1024)
                server_msg = pickle.loads(rdata)
                assert isinstance(server_msg, ServerMsgRoundStart)

                round = server_msg.round_num

                logger.info(f"Received from the server : {server_msg}")
                move = rps_client_player.next_move(round)
                msg_move = ClientMsgRoundMove(move)
                data = pickle.dumps(msg_move)
                logger.info(f"Sending to server : {msg_move}")
                s.send(data)
                game_rounds_counter += 1

                rdata = s.recv(1024)
                round_result = pickle.loads(rdata)
                assert isinstance(round_result, ServerMsgRoundResult)
                logger.info(f"Result: {round_result.result}")

                client_OK = ClientMsgOK("Received server round result")
                data = pickle.dumps(client_OK)
                s.send(data)

                rps_client_player.game_result(
                    round,
                    round_result.player_one_id,
                    round_result.player_one_move,
                    round_result.player_two_id,
                    round_result.player_two_move,
                    round_result.result,
                )

                # Find player and bot ids
                if round_result.player_one_id == my_id:
                    p_choice = round_result.player_one_move
                    b_choice = round_result.player_two_move
                else:
                    p_choice = round_result.player_two_move
                    b_choice = round_result.player_one_move

                # Add result to logs
                result = round_result.result
                if player_class_name != "RPSSimpleBotPlayer":
                    log_result = [p_choice, b_choice, result, server_host, server_port, player_class_name, i_am_a_bot, my_id]
                    msg_data = ""
                    for data in log_result:
                        msg_data += f"{data},"
                    msg_data = msg_data[:-1]+"\n"
                    with open(f'logs/result_log.csv', 'a', encoding='UTF-8') as the_file:
                        the_file.write(msg_data)

                rdata = s.recv(1024)
                server_msg = pickle.loads(rdata)
                logger.info(server_msg)

                if isinstance(server_msg, ServerMsgPrepareForNextRound):
                    logger.info(f"Preparing for next round: {server_msg.round_num}")
                    client_OK = ClientMsgOK("Received preparing for next round")
                    data = pickle.dumps(client_OK)
                    s.send(data)
                elif isinstance(server_msg, ServerMsgExitClient):
                    logger.info(f"Played {game_rounds_counter} game rounds")
                    print(f"Played {game_rounds_counter} game rounds")
                    print(f"Game summary: {server_msg.counters}")
                    outcome_counters = {"W": 0, "D": 0, "L": 0}
                    for k in server_msg.counters:
                        if k == my_id:
                            outcome_counters["W"] = server_msg.counters[k]
                        elif k == -1:
                            outcome_counters["D"] = server_msg.counters[k]
                        else:
                            outcome_counters["L"] = server_msg.counters[k]
                    print(f"W: {outcome_counters['W']}")
                    print(f"D: {outcome_counters['D']}")
                    print(f"L: {outcome_counters['L']}")



                    logger.info(f"Exit command from server: {server_msg}, exiting ...")
                    print("Exit command from server. Exiting ...")
                    game_ended = True
                else:
                    logger.error(f"Unexpected server msg type {server_msg}")
                    raise Exception("Unexpected server msg type")

        s.close()


