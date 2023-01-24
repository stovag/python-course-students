# Compute outcome
import pickle

from assignment02.rps_game.rps_messages import ServerMsgRoundStart, ServerMsgDuelReadyToStart, ServerMsgRoundResult, \
    ServerMsgExitClient, ServerMsgPrepareForNextRound


def game_logic(client_list, client_moves):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    move0 = client_moves[0].move
    id0 = client_list[0].client_id
    move1 = client_moves[1].move
    id1 = client_list[1].client_id

    if move0 == move1:
        winner = "draw"
    elif move0 == rock:
        if move1 == paper:
            winner = id1
        else:
            winner = id0
    elif move0 == scissors:
        if move1 == rock:
            winner = id1
        else:
            winner = id0
    elif move0 == paper:
        if move1 == scissors:
            winner = id1
        else:
            winner = id0
    return winner

def serve_duel(duel_client_list, game_rounds):

    # Inform clients that the duel is ready to start
    for client in duel_client_list:
        duel_ready_msg = ServerMsgDuelReadyToStart()
        data = pickle.dumps(duel_ready_msg)
        client.socket.send(data)
        data = client.socket.recv(1024)
        client_OK = pickle.loads(data)
        print(f'Received: {client_OK} from {client}')

    # Play a game
    for rps_round in range(game_rounds):
        for client in duel_client_list:
            play_game_msg = ServerMsgRoundStart(rps_round)
            data = pickle.dumps(play_game_msg)
            client.socket.send(data)
            print(f'Sending ServerMsgRoundStart to {client}')

        # Receive the move of each client
        client_moves = []

        for client in duel_client_list:
            print(f'Waiting for the move of {client}')
            data = client.socket.recv(1024)
            client_move_msg = pickle.loads(data)
            client_moves.append(client_move_msg)
            move = client_move_msg.move
            print(f'Received: {client_move_msg}')

        winner = game_logic(duel_client_list, client_moves)
        round_result_msg = ServerMsgRoundResult(duel_client_list[0].client_id, duel_client_list[1].client_id, winner)

        # Send the outcome
        for client in duel_client_list:
            data = pickle.dumps(round_result_msg)
            client.socket.send(data)
            print(f'Sending Round result to {client}')

        # Send the outcome
        for client in duel_client_list:
            data = client.socket.recv(1024)
            client_result_msg = pickle.loads(data)
            print(f'Received: {client_result_msg}')

        if rps_round < game_rounds-1:
            for client in duel_client_list:
                exit_msg = ServerMsgPrepareForNextRound(rps_round+1)
                data = pickle.dumps(exit_msg)
                client.socket.send(data)
                print(f'Sending prepare for next round {rps_round+1} msg to {client}')
        else:
            # Terminate clients
            for client in duel_client_list:
                exit_msg = ServerMsgExitClient(client.client_id, "Exit")
                data = pickle.dumps(exit_msg)
                client.socket.send(data)
                print(f'Sending Exit msg to {client}')